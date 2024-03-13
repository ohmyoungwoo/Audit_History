import './app.css'

import 'bootstrap/dist/css/bootstrap.min.css'
//import 'bootstrap/dist/js/bootstrap.min.js'  // 작동 안됨. 이유를 모름

import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		name: 'world'
	}
//	target: document.getElementById('app')  // 작동 안됨. 이유를 모름
});

export default app;