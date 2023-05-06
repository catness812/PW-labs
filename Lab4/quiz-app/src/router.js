import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from './components/LandingPage.vue';
import SignUp from './components/SignUpPage.vue';
import Login from './components/LoginPage.vue';
import Welcome from './components/WelcomePage.vue';
import Quiz from './components/QuizPage.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingPage
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/welcome/:id',
      name: 'welcome',
      component: Welcome,
      props: true,
      beforeEnter: (to, _from, next) => {
        const isLoggedIn = sessionStorage.getItem('isLogged');
        const userID = sessionStorage.getItem('id');
        if (!isLoggedIn) {
            next({ name: 'landing' });
          } else if (to.params.id !== userID) {
            next({ name: 'landing' });
          } else {
            next();
          }
      }
    },
    {
      path: '/quizzes/:id',
      name: 'quiz',
      component: Quiz,
      props: true,
      beforeEnter: (_to, _from, next) => {
        const isLoggedIn = sessionStorage.getItem('isLogged');
        if (!isLoggedIn) {
            next({ name: 'landing' });
          } else {
            next();
          }
      }
    }
  ]
});

export default router;
