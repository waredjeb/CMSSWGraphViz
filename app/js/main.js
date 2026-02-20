/**
 * main.js - Application initialization
 * Loads data and initializes all modules
 */

// Global data storage
window.bundleData = null;

/**
 * Initialize the application
 */
async function initApp() {
    console.log('Initializing CMSSW Graph Visualization...');

    try {
        // Show loading indicator
        showLoading(true);

        // Load bundle data
        const response = await fetch('../data/bundle.json');
        if (!response.ok) {
            throw new Error(`Failed to load bundle.json: ${response.statusText}`);
        }

        window.bundleData = await response.json();
        console.log('Bundle data loaded:', {
            nodes: window.bundleData.nodes.length,
            edges: window.bundleData.edges.length,
            modules: Object.keys(window.bundleData.modules).length
        });

        // Initialize graph
        GraphManager.init(window.bundleData);

        // Initialize UI components
        PanelManager.init();
        SearchManager.init();
        EgoGraphManager.init();
        DependencyExplorer.init();
        KeyboardNav.init();
        FilterManager.init();
        UploadManager.init();

        // Update stats
        updateStats({
            nodeCount: window.bundleData.nodes.length,
            edgeCount: window.bundleData.edges.length,
            moduleCount: Object.keys(window.bundleData.modules).length
        });

        // Hide loading indicator
        showLoading(false);

        // Fit graph to viewport
        GraphManager.fit();

        console.log('Application initialized successfully');

    } catch (error) {
        console.error('Error initializing application:', error);
        showLoading(false);
        alert(`Failed to initialize application: ${error.message}`);
    }
}

/**
 * Show/hide loading indicator
 */
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

/**
 * Update statistics display
 */
function updateStats(stats) {
    document.getElementById('node-count').textContent = `Nodes: ${stats.nodeCount}`;
    document.getElementById('edge-count').textContent = `Edges: ${stats.edgeCount}`;
    document.getElementById('module-count').textContent = `Modules: ${stats.moduleCount}`;
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);
