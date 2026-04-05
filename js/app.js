// ==================== AGENTS DATA ====================
const agentsData = [
    {
        id: 'chatbot-pro',
        name: 'ChatBot Pro',
        creator: 'BotFactory',
        desc: 'Chatbot IA avancé pour site web. Répond aux visiteurs, qualifie les leads et prend des RDV 24/7.',
        icon: 'fas fa-comments',
        color: '#667eea,#764ba2',
        tags: ['💬 Chat', '🌐 Web', '🤖 Auto'],
        rating: 4.7,
        users: '1.1K',
        price: 'free',
        priceLabel: 'Gratuit',
        upvotes: 384,
        category: 'support',
        isNew: true
    },
    {
        id: 'email-genius',
        name: 'Email Genius AI',
        creator: 'MailCraft',
        desc: 'Rédige des emails de prospection personnalisés avec un taux de réponse 4x supérieur à la moyenne.',
        icon: 'fas fa-envelope',
        color: '#f093fb,#f5576c',
        tags: ['📧 Email', '✍️ Rédaction', '🎯 Outreach'],
        rating: 4.6,
        users: '890',
        price: 'paid',
        priceLabel: 'Dès 29€/mois',
        upvotes: 312,
        category: 'email',
        isNew: false
    },
    {
        id: 'seo-master',
        name: 'SEO Master AI',
        creator: 'RankBoost',
        desc: 'Analyse votre SEO, trouve les mots-clés rentables et rédige du contenu optimisé pour Google.',
        icon: 'fas fa-chart-line',
        color: '#4facfe,#00f2fe',
        tags: ['🔍 SEO', '📝 Contenu', '📊 Analytics'],
        rating: 4.8,
        users: '2.1K',
        price: 'paid',
        priceLabel: 'Dès 39€/mois',
        upvotes: 567,
        category: 'seo',
        isNew: false
    },
    {
        id: 'recruteur-ia',
        name: 'Recruteur IA',
        creator: 'HRTech',
        desc: 'Trie les CV, pré-qualifie les candidats et planifie les entretiens automatiquement.',
        icon: 'fas fa-user-tie',
        color: '#a18cd1,#fbc2eb',
        tags: ['👥 RH', '📋 CV', '🤝 Recrutement'],
        rating: 4.5,
        users: '650',
        price: 'paid',
        priceLabel: 'Dès 79€/mois',
        upvotes: 245,
        category: 'rh',
        isNew: true
    },
    {
        id: 'compta-bot',
        name: 'ComptaBot',
        creator: 'FinanceAI',
        desc: 'Automatise votre comptabilité : factures, rapprochements bancaires, TVA et bilans.',
        icon: 'fas fa-calculator',
        color: '#13547a,#80d0c7',
        tags: ['💼 Finance', '📊 Compta', '🧾 Factures'],
        rating: 4.4,
        users: '430',
        price: 'paid',
        priceLabel: 'Dès 49€/mois',
        upvotes: 198,
        category: 'finance',
        isNew: false
    },
    {
        id: 'design-ai',
        name: 'DesignCraft AI',
        creator: 'CreativeHub',
        desc: 'Génère des visuels, logos et maquettes professionnels à partir de simples descriptions.',
        icon: 'fas fa-palette',
        color: '#ff6b6b,#feca57',
        tags: ['🎨 Design', '🖼️ Visuel', '✨ Créatif'],
        rating: 4.7,
        users: '1.5K',
        price: 'free',
        priceLabel: 'Freemium',
        upvotes: 423,
        category: 'design',
        isNew: true
    },
    {
        id: 'legal-assistant',
        name: 'Legal Assistant AI',
        creator: 'JuriTech',
        desc: 'Analyse vos contrats, détecte les clauses à risque et génère des documents juridiques.',
        icon: 'fas fa-scale-balanced',
        color: '#c471f5,#fa71cd',
        tags: ['⚖️ Juridique', '📄 Contrats', '🔒 Conformité'],
        rating: 4.6,
        users: '320',
        price: 'paid',
        priceLabel: 'Dès 99€/mois',
        upvotes: 276,
        category: 'juridique',
        isNew: false
    },
    {
        id: 'social-pilot',
        name: 'Social Pilot AI',
        creator: 'SocialStack',
        desc: 'Planifie, rédige et publie vos posts sur tous les réseaux sociaux avec optimisation IA.',
        icon: 'fas fa-share-nodes',
        color: '#43e97b,#38f9d7',
        tags: ['📱 Social', '📅 Planning', '✍️ Contenu'],
        rating: 4.5,
        users: '980',
        price: 'free',
        priceLabel: 'Essai gratuit',
        upvotes: 356,
        category: 'marketing',
        isNew: false
    },
    {
        id: 'code-assistant',
        name: 'CodeBuddy AI',
        creator: 'DevTools Inc',
        desc: 'Assistant de développement IA qui code, debug et optimise votre code en temps réel.',
        icon: 'fas fa-code',
        color: '#667eea,#764ba2',
        tags: ['💻 Dev', '🐛 Debug', '⚡ Opti'],
        rating: 4.9,
        users: '3.2K',
        price: 'free',
        priceLabel: 'Gratuit',
        upvotes: 891,
        category: 'dev',
        isNew: true
    },
    {
        id: 'translator-pro',
        name: 'TranslatePro AI',
        creator: 'LinguaAI',
        desc: 'Traduction professionnelle en 50+ langues avec préservation du ton et du contexte métier.',
        icon: 'fas fa-language',
        color: '#f093fb,#f5576c',
        tags: ['🌍 Traduction', '📝 Contenu', '🗣️ Multilingue'],
        rating: 4.7,
        users: '1.8K',
        price: 'paid',
        priceLabel: 'Dès 19€/mois',
        upvotes: 445,
        category: 'marketing',
        isNew: false
    },
    {
        id: 'data-analyst',
        name: 'DataSense AI',
        creator: 'AnalyticsLab',
        desc: 'Analyse vos données, génère des rapports visuels et détecte les tendances automatiquement.',
        icon: 'fas fa-chart-pie',
        color: '#4facfe,#00f2fe',
        tags: ['📊 Data', '📈 Analytics', '🔮 Prédiction'],
        rating: 4.8,
        users: '1.4K',
        price: 'paid',
        priceLabel: 'Dès 59€/mois',
        upvotes: 534,
        category: 'dev',
        isNew: false
    },
    {
        id: 'voice-clone',
        name: 'VoiceClone AI',
        creator: 'AudioTech',
        desc: 'Clone votre voix et génère des audios naturels pour vos podcasts, vidéos et présentations.',
        icon: 'fas fa-microphone',
        color: '#a18cd1,#fbc2eb',
        tags: ['🎙️ Vocal', '🎧 Audio', '🎬 Vidéo'],
        rating: 4.6,
        users: '760',
        price: 'paid',
        priceLabel: 'Dès 29€/mois',
        upvotes: 387,
        category: 'vocal',
        isNew: true
    }
];

let currentFilter = 'all';
let displayedAgents = 6;

// ==================== DOM READY ====================
document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initSearch();
    initStats();
    initUpvotes();
    initAgentsList();
    initFilters();
    initForms();
    initAnimations();
    initCookieBanner();
});

// ==================== NAVBAR ====================
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');

    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });
    }

    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = mobileToggle.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        });
    }
}

// ==================== SEARCH ====================
function initSearch() {
    const searchInput = document.getElementById('heroSearch');
    const suggestions = document.querySelectorAll('.suggestion');

    suggestions.forEach(s => {
        s.addEventListener('click', () => {
            if (searchInput) {
                searchInput.value = s.dataset.query;
                searchInput.focus();
                filterAgentsBySearch(s.dataset.query);
            }
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterAgentsBySearch(e.target.value);
        });
    }

    const searchBtn = document.querySelector('.search-btn');
    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            if (searchInput) {
                filterAgentsBySearch(searchInput.value);
                const explorer = document.getElementById('explorer');
                if (explorer) explorer.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
}

function filterAgentsBySearch(query) {
    if (!query) {
        renderAgentsList(agentsData);
        return;
    }
    const q = query.toLowerCase();
    const filtered = agentsData.filter(a =>
        a.name.toLowerCase().includes(q) ||
        a.desc.toLowerCase().includes(q) ||
        a.tags.some(t => t.toLowerCase().includes(q)) ||
        a.category.toLowerCase().includes(q)
    );
    renderAgentsList(filtered);
}

// ==================== STATS COUNTER ====================
function initStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    if (!statNumbers.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCount(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(el => observer.observe(el));
}

function animateCount(el) {
    // Skip elements without data-count (text stats like "24/7", "<3s", etc.)
    if (!el.dataset.count) return;
    const target = parseInt(el.dataset.count);
    if (isNaN(target)) return;
    const suffix = el.dataset.suffix || '';
    const duration = 2000;
    const start = performance.now();

    function update(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.floor(target * eased).toLocaleString('fr-CH') + suffix;
        if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
}

// ==================== UPVOTES ====================
function initUpvotes() {
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-upvote');
        if (!btn) return;

        btn.classList.toggle('voted');
        const countEl = btn.querySelector('.upvote-count');
        if (countEl) {
            let count = parseInt(countEl.textContent);
            countEl.textContent = btn.classList.contains('voted') ? count + 1 : count - 1;
        }
    });
}

// ==================== AGENTS LIST ====================
function initAgentsList() {
    renderAgentsList(agentsData);

    const loadMoreBtn = document.getElementById('loadMore');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            displayedAgents += 6;
            const filtered = getFilteredAgents();
            renderAgentsList(filtered);
            if (displayedAgents >= filtered.length) {
                loadMoreBtn.style.display = 'none';
            }
        });
    }
}

function getFilteredAgents() {
    let filtered = [...agentsData];
    switch (currentFilter) {
        case 'free':
            filtered = filtered.filter(a => a.price === 'free');
            break;
        case 'paid':
            filtered = filtered.filter(a => a.price === 'paid');
            break;
        case 'new':
            filtered = filtered.filter(a => a.isNew);
            break;
        case 'top':
            filtered.sort((a, b) => b.upvotes - a.upvotes);
            break;
    }
    return filtered;
}

function renderAgentsList(agents) {
    const list = document.getElementById('agentsList');
    if (!list) return;

    const toShow = agents.slice(0, displayedAgents);
    list.innerHTML = toShow.map(agent => `
        <div class="agent-list-item" data-category="${agent.category}">
            <div class="agent-avatar" style="background: linear-gradient(135deg, ${agent.color});">
                <i class="${agent.icon}"></i>
            </div>
            <div class="agent-list-info">
                <h3>${agent.name} ${agent.isNew ? '<span class="tag" style="font-size:0.7rem;">🆕 Nouveau</span>' : ''}</h3>
                <p>${agent.desc}</p>
            </div>
            <div class="agent-list-tags">
                ${agent.tags.map(t => `<span class="tag">${t}</span>`).join('')}
            </div>
            <div class="agent-list-actions">
                <button class="btn-upvote" data-id="${agent.id}">
                    <i class="fas fa-arrow-up"></i>
                    <span class="upvote-count">${agent.upvotes}</span>
                </button>
                <a href="agent.html?id=${agent.id}" class="btn-try">
                    Voir <i class="fas fa-arrow-right"></i>
                </a>
            </div>
        </div>
    `).join('');

    // Show/hide load more
    const loadMoreBtn = document.getElementById('loadMore');
    if (loadMoreBtn) {
        loadMoreBtn.style.display = displayedAgents >= agents.length ? 'none' : 'inline-flex';
    }
}

// ==================== FILTERS ====================
function initFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            displayedAgents = 6;
            const filtered = getFilteredAgents();
            renderAgentsList(filtered);
        });
    });
}

// ==================== FORMS ====================
function initForms() {
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = newsletterForm.querySelector('button');
            btn.textContent = '✅ Inscrit !';
            btn.style.background = '#00D68F';
            setTimeout(() => {
                btn.textContent = "S'abonner gratuitement";
                btn.style.background = '';
                newsletterForm.reset();
            }, 3000);
        });
    }

    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = contactForm.querySelector('button');
            btn.innerHTML = '✅ Demande envoyée !';
            btn.style.background = '#00D68F';
            setTimeout(() => {
                btn.innerHTML = 'Réserver mon appel gratuit <i class="fas fa-calendar-check"></i>';
                btn.style.background = '';
                contactForm.reset();
            }, 3000);
        });
    }

    const submitForm = document.getElementById('submitAgentForm');
    if (submitForm) {
        submitForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = submitForm.querySelector('button[type="submit"]');
            btn.innerHTML = '✅ Agent soumis avec succès !';
            btn.style.background = '#00D68F';
            setTimeout(() => {
                btn.innerHTML = 'Soumettre mon agent <i class="fas fa-paper-plane"></i>';
                btn.style.background = '';
                submitForm.reset();
            }, 3000);
        });
    }
}

// ==================== ANIMATIONS ====================
function initAnimations() {
    const elements = document.querySelectorAll('.agent-card, .category-card, .solution-card, .testimonial-card, .blog-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    elements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

// ==================== COOKIE BANNER ====================
function initCookieBanner() {
    const banner = document.getElementById('cookieBanner');
    const acceptBtn = document.getElementById('cookieAccept');
    const declineBtn = document.getElementById('cookieDecline');

    if (!banner) return;

    // Check if already accepted/declined
    if (localStorage.getItem('ai_cookies')) {
        banner.classList.add('hidden');
        return;
    }

    acceptBtn.addEventListener('click', () => {
        localStorage.setItem('ai_cookies', 'accepted');
        banner.classList.add('hidden');
        if (typeof gtag === 'function') {
            gtag('consent', 'update', { analytics_storage: 'granted' });
        }
    });

    declineBtn.addEventListener('click', () => {
        localStorage.setItem('ai_cookies', 'declined');
        banner.classList.add('hidden');
        window['ga-disable-G-B5627RD3TF'] = true;
    });
}