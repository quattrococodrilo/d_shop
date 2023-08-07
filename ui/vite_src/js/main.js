import "vite/modulepreload-polyfill";
import "../css/main.css";
import Alpine from "alpinejs";
import axios from 'axios';

window.axios = axios;
const csrfToken = document.querySelector('[name=csrf-token]').content;
window.axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

window.Alpine = Alpine;
Alpine.start();

