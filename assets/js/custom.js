// Custom JavaScript per migliorare la navigazione

// Highlight della sezione corrente nel TOC
document.addEventListener('DOMContentLoaded', function() {
  // Funzione per evidenziare la sezione corrente nel TOC
  function highlightCurrentSection() {
    const sections = document.querySelectorAll('.md-content h1, .md-content h2, .md-content h3');
    const tocLinks = document.querySelectorAll('.md-nav__link');
    
    // Trova la sezione visibile
    let currentSection = '';
    const scrollPosition = window.scrollY + 100; // Offset per anticipare
    
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      if (scrollPosition >= sectionTop) {
        currentSection = section.id || section.textContent.trim();
      }
    });
    
    // Rimuovi highlight da tutti i link
    tocLinks.forEach(link => {
      link.classList.remove('md-nav__link--active');
    });
    
    // Evidenzia il link corrente
    if (currentSection) {
      tocLinks.forEach(link => {
        if (link.getAttribute('href') === '#' + currentSection) {
          link.classList.add('md-nav__link--active');
          // Scroll del TOC per mostrare il link attivo
          link.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      });
    }
  }
  
  // Aggiorna l'highlight durante lo scroll
  let ticking = false;
  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        highlightCurrentSection();
        ticking = false;
      });
      ticking = true;
    }
  });
  
  // Esegui all'inizio
  highlightCurrentSection();
  
  // Migliora il pulsante "Back to top"
  const backToTopButton = document.querySelector('.md-top');
  if (backToTopButton) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 300) {
        backToTopButton.style.display = 'block';
        backToTopButton.style.opacity = '0.8';
      } else {
        backToTopButton.style.opacity = '0';
      }
    });
  }
  
  // Smooth scroll per i link interni
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href.length > 1) {
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          const offsetTop = target.offsetTop - 60; // Offset per l'header
          window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
          });
          // Aggiorna l'URL senza ricaricare la pagina
          history.pushState(null, null, href);
        }
      }
    });
  });
  
  // Migliora la visibilità del TOC su mobile
  if (window.innerWidth <= 768) {
    const tocToggle = document.querySelector('.md-nav__title');
    if (tocToggle) {
      tocToggle.addEventListener('click', function() {
        const toc = document.querySelector('.md-nav--secondary');
        if (toc) {
          toc.classList.toggle('md-nav--visible');
        }
      });
    }
  }
  
  // Aggiungi indicatori di progresso per le sezioni lunghe
  const progressBar = document.createElement('div');
  progressBar.className = 'reading-progress';
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: var(--md-primary-fg-color);
    z-index: 1000;
    transition: width 0.1s;
    width: 0%;
  `;
  document.body.appendChild(progressBar);
  
  // Calcola e aggiorna la barra di progresso
  function updateProgressBar() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    const scrollTop = window.scrollY;
    const progress = (scrollTop / (documentHeight - windowHeight)) * 100;
    progressBar.style.width = progress + '%';
  }
  
  window.addEventListener('scroll', updateProgressBar);
  updateProgressBar();
});

// Migliora la ricerca
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.querySelector('input[type="search"]');
  if (searchInput) {
    searchInput.setAttribute('placeholder', 'Cerca nella documentazione...');
  }
});

