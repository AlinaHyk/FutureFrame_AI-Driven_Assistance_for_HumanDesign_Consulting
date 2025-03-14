// Check if service workers are supported
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/static/service-worker.js')
        .then(registration => {
          console.log('ServiceWorker registration successful');
        })
        .catch(error => {
          console.error('ServiceWorker registration failed:', error);
        });
    });
  }
  
  // Add install prompt
  let deferredPrompt;
  const installButton = document.createElement('button');
  installButton.style.display = 'none';
  installButton.textContent = 'Install App';
  
  window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;
    // Update UI notify the user they can install the PWA
    installButton.style.display = 'block';
    
    installButton.addEventListener('click', (e) => {
      // Hide our user interface that shows our install button
      installButton.style.display = 'none';
      // Show the install prompt
      deferredPrompt.prompt();
      // Wait for the user to respond to the prompt
      deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
          console.log('User accepted the install prompt');
        } else {
          console.log('User dismissed the install prompt');
        }
        deferredPrompt = null;
      });
    });
    
    // Add the install button to the UI
    document.body.appendChild(installButton);
  });