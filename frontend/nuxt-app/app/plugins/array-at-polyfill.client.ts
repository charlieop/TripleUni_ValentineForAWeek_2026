export default defineNuxtPlugin(() => {
  // Polyfill for Array.prototype.at() - required by vue-router 4
  // This must run before vue-router initializes
  if (!Array.prototype.at) {
    Array.prototype.at = function (index: number) {
      index = Math.trunc(index) || 0;
      if (index < 0) index += this.length;
      return this[index];
    };
  }
});
