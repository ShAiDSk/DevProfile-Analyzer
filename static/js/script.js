let myChart = null;
let langChart = null;
// Store current user stats globally so we can send them to AI
let currentUserStats = null;

async function analyzeProfile() {
    const handle = document.getElementById('handle').value;
    const platform = document.getElementById('platform').value;
    const loader = document.getElementById('loader');
    const result = document.getElementById('result');

    if (!handle) return alert("Please enter a handle!");

    loader.classList.remove('hidden');
    result.classList.add('hidden');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ platform, handle })
        });

        const res = await response.json();

        if (res.success) {
            updateUI(res.data);
            minimizeSearchUI();
            result.classList.remove('hidden');
        } else {
            alert(res.message);
        }
    } catch (error) {
        alert("Server Error. Check console.");
        console.error(error);
    } finally {
        loader.classList.add('hidden');
    }
}

function updateUI(user) {
    currentUserStats = user;
    const isGitHub = document.getElementById('platform').value === 'GitHub';
    
    // --- MAIN UI UPDATES ---
    document.getElementById('username').innerText = user.handle;
    document.getElementById('rank').innerText = user.rank || "N/A";
    document.getElementById('ratingLabel').innerText = isGitHub ? "Total Stars" : "Rating";
    document.getElementById('maxLabel').innerText = isGitHub ? "Public Repos" : "Max Rating";
    
    // Stats Numbers
    document.getElementById('rating').innerText = user.rating;
    document.getElementById('maxRating').innerText = user.maxRating;

    // ✨ Update Solved Count (Main UI)
    document.getElementById('solvedVal').innerText = user.solved !== undefined ? user.solved : "N/A";

    document.getElementById('avatar').src = user.avatar;

    // Badges
    const badgeContainer = document.getElementById('badges-container');
    badgeContainer.innerHTML = ''; 
    if (user.badges && user.badges.length > 0) {
        user.badges.forEach(badge => {
            const span = document.createElement('span');
            span.className = "bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-bold px-3 py-1 rounded-full text-sm shadow-lg hover:scale-110 transition";
            span.innerText = badge;
            badgeContainer.appendChild(span);
        });
    }

    // Persona
    if (user.persona) {
        document.getElementById('personaTitle').innerText = user.persona.title;
        document.getElementById('personaDesc').innerText = user.persona.description;
        document.getElementById('powerValue').innerText = user.persona.level + "/100";
        setTimeout(() => document.getElementById('powerBar').style.width = user.persona.level + "%", 300);
    }

    // --- CAPTURE ZONE UPDATES ---
    document.getElementById('cap-username').innerText = user.handle;
    document.getElementById('cap-rank').innerText = user.rank || "N/A";
    document.getElementById('cap-rating').innerText = user.rating;
    document.getElementById('cap-maxRating').innerText = user.maxRating;
    document.getElementById('cap-solved').innerText = user.solved !== undefined ? user.solved : "N/A";
    document.getElementById('cap-avatar').src = user.avatar;
    
    if (user.persona) {
        document.getElementById('cap-personaTitle').innerText = user.persona.title;
        document.getElementById('cap-personaDesc').innerText = user.persona.description;
        document.getElementById('cap-powerValue').innerText = user.persona.level + "/100";
        document.getElementById('cap-powerBar').style.width = user.persona.level + "%";
    }
    
    // Capture Badges
    const capBadgeContainer = document.getElementById('cap-badges');
    capBadgeContainer.innerHTML = ''; 
    if (user.badges && user.badges.length > 0) {
        user.badges.forEach(badge => {
            const span = document.createElement('span');
            span.className = "bg-yellow-600/20 border border-yellow-500/50 text-yellow-200 px-3 py-1 rounded-full text-sm";
            span.innerText = badge;
            capBadgeContainer.appendChild(span);
        });
    }

    // Render Charts
    renderChart(user.ratingHistory, user.contestHistory);
    
    const langContainer = document.getElementById('langChartContainer');
    if (user.languages) {
        langContainer.classList.remove('hidden');
        renderLangChart(user.languages);
    } else {
        langContainer.classList.add('hidden');
    }
}

// ✨ UPDATED AI FUNCTION
async function askAI(mode) {
    if (!currentUserStats) return alert("Analyze a profile first!");

    const aiBox = document.getElementById('ai-result-box');
    const aiText = document.getElementById('aiOutput');
    const roastBtn = document.getElementById('roastBtn');
    const hypeBtn = document.getElementById('hypeBtn');
    
    const activeBtn = mode === 'roast' ? roastBtn : hypeBtn;
    const originalText = mode === 'roast' ? "🔥 Roast Me (AI)" : "🚀 Hype Me (AI)";

    activeBtn.innerHTML = `<span class="animate-spin inline-block mr-2">⏳</span> Cooking...`;
    activeBtn.disabled = true;
    
    aiBox.classList.remove('hidden');
    aiText.innerText = "🤖 AI is thinking...";
    aiText.classList.add('animate-pulse');
    aiBox.className = "md:col-span-2 bg-black/40 border border-gray-600 p-6 rounded-2xl relative mt-4"; 

    try {
        const response = await fetch('/ask-ai', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                mode: mode, 
                stats: currentUserStats 
            })
        });

        const res = await response.json();
        
        aiText.classList.remove('animate-pulse');
        aiBox.className = `md:col-span-2 bg-black/40 border-l-4 p-6 rounded-2xl relative mt-4 ${mode === 'roast' ? 'border-red-500' : 'border-blue-500'}`;
        
        typeWriter(res.message, aiText);

    } catch (error) {
        aiText.innerText = "AI Error. Check console.";
        console.error(error);
    } finally {
        activeBtn.innerHTML = originalText;
        activeBtn.disabled = false;
    }
}

function typeWriter(text, element) {
    element.innerText = "";
    let i = 0;
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, 30);
        }
    }
    type();
}

function renderChart(dataPoints, labels) {
    const ctx = document.getElementById('ratingChart').getContext('2d');
    if (myChart) myChart.destroy();

    const isLeetCode = document.getElementById('platform').value === 'LeetCode';

    myChart = new Chart(ctx, {
        type: isLeetCode ? 'bar' : 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Stats',
                data: dataPoints,
                borderColor: '#818cf8',
                backgroundColor: isLeetCode ? ['#22c55e', '#eab308', '#ef4444'] : 'rgba(129, 140, 248, 0.2)',
                borderWidth: 2,
                tension: 0.4,
                fill: !isLeetCode,
                pointRadius: isLeetCode ? 0 : 3
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: { display: false },
                y: { grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#9ca3af' } }
            }
        }
    });
}

function renderLangChart(languages) {
    const ctx = document.getElementById('langChart').getContext('2d');
    if (langChart) langChart.destroy();

    langChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(languages),
            datasets: [{
                data: Object.values(languages),
                backgroundColor: ['#F59E0B', '#3B82F6', '#10B981', '#EF4444', '#8B5CF6'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'right', labels: { color: 'white' } } }
        }
    });
}

function downloadProfile() {
    const captureZone = document.getElementById('capture-zone');
    captureZone.classList.remove('invisible'); 
    
    html2canvas(captureZone, {
        backgroundColor: "#0f172a",
        scale: 2,
        useCORS: true 
    }).then(canvas => {
        const link = document.createElement('a');
        link.download = `DevProfile-${document.getElementById('username').innerText}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
        captureZone.classList.add('invisible');
    }).catch(err => {
        console.error(err);
        alert("Download failed. See console.");
        captureZone.classList.add('invisible');
    });
}

// --- 👇 THIS WAS MISSING: NAVBAR FUNCTIONALITY 👇 ---
function setPlatform(name) {
    const select = document.getElementById('platform');
    select.value = name;
    
    const input = document.getElementById('handle');
    input.focus();
    input.placeholder = `Enter ${name} username...`;
    
    // Animation to show visual feedback
    input.classList.add('ring-2', 'ring-purple-500');
    setTimeout(() => input.classList.remove('ring-2', 'ring-purple-500'), 300);
}


// --- ✨ NEW: UI MINIMIZER ✨ ---
function minimizeSearchUI() {
    const hero = document.getElementById('hero-section');
    const card = document.getElementById('search-card');
    const inputs = document.getElementById('search-inputs');
    const handleInput = document.getElementById('handle');
    const platformSelect = document.getElementById('platform');
    const btn = card.querySelector('button');

    // 1. Hide the Big Hero Title smoothly
    hero.style.display = 'none';

    // 2. Transform the Card (Make it a wide horizontal bar)
    card.classList.remove('max-w-xl', 'p-8', 'rounded-3xl', 'hover:scale-[1.01]');
    card.classList.add('w-full', 'max-w-6xl', 'p-4', 'rounded-2xl', 'mb-6');
    
    // 3. Transform Inputs to a Row (Side-by-Side)
    // We keep flex-col on mobile, but switch to flex-row on desktop
    inputs.classList.remove('flex-col', 'gap-5');
    inputs.classList.add('flex-col', 'md:flex-row', 'gap-4', 'items-center');

    // 4. Adjust Input Widths for the Bar Layout
    // Make the button smaller and fit the row
    btn.classList.remove('w-full', 'py-4');
    btn.classList.add('w-full', 'md:w-auto', 'px-8', 'py-3', 'whitespace-nowrap');
    
    // Make inputs take available space
    handleInput.parentElement.classList.add('w-full');
    platformSelect.parentElement.classList.add('w-full', 'md:w-64'); // Limit dropdown width
}