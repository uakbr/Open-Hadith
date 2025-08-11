/** @type {import('@sveltejs/kit').Config} */
import adapter from '@sveltejs/adapter-netlify';
const config = {
	kit: {
		adapter: adapter(), // currently the adapter does not take any options
		// hydrate the <div id="svelte"> element in src/app.html
		// target: '#svelte'
		vite: {
			server: {
				proxy: {
					'/api': {
						target: 'http://127.0.0.1:5000',
						changeOrigin: true,
						secure: false
					}
				}
			}
		}
	}
};

export default config;
