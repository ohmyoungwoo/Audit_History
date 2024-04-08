<script>
	import Router from 'svelte-spa-router'
	import Home from "./routes/Home.svelte"
	import Detail from "./routes/Detail.svelte"
	import QuestionCreate from './routes/QuestionCreate.svelte'
	import QuestionModify from "./routes/QuestionModify.svelte"
	import Navigation from './components/Navigation.svelte'
	import UserCreate from "./routes/UserCreate.svelte"
	import UserLogin from "./routes/UserLogin.svelte"

	import FileUpload from './routes/file_upload.svelte'
  
	const routes = {
	  '/': Home,
	  '/detail/:question_id': Detail,
	  '/question-create': QuestionCreate,
	  '/question-modify/:question_id': QuestionModify,
	  '/user-create': UserCreate,
	  '/user-login': UserLogin,
	  '/api/question-create/file' : FileUpload,
	}
  </script>
  
  <Navigation/>
  <Router {routes}/>