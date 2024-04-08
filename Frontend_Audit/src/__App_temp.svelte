<script>
	import Router from 'svelte-spa-router'
	import Home from "./routes/Home.svelte"
	import file_upload from "./routes/file_upload.svelte"
	import file_upload2 from "./routes/file_upload2.svelte"
	import file_upload3 from "./routes/file_upload3.svelte"
	import detail from "./routes/Detail.svelte"

	const routes = {
	//  '/': Home,
	//  '/': file_upload2
	//  '/': detail,
	'/': file_upload3
	}
  </script>

  <Router {routes}/>