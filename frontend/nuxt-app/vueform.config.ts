import vueform from '@vueform/vueform/dist/vueform'
import { defineConfig } from '@vueform/vueform'
import zh from "./vueform/locales/zh_CN";

// You might place these anywhere else in your project
import '@vueform/vueform/dist/vueform.css';

export default defineConfig({
  theme: vueform,
  locales: { zh },
  locale: 'zh',
})