const content = require("./content.js");
const theme = require("./theme.js");
const pluginsStatic = require("./plugins.js");
const AppsToRender = require("./scripts/apps_finder.js");

let [apps, plugins] = AppsToRender("./apps");

apps = apps ? apps : [];
plugins = plugins ? plugins : [];

let pluginsToAdd = plugins.map((plugin) => {
  return require(plugin);
});

if (apps.length > 0) {
  console.log("Apps to render:");
  console.log(apps.join("\n"));
}

if (pluginsToAdd.length > 0) {
  console.log("Plugins to add:");
  console.log(pluginsToAdd.join("\n"));
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [...content, ...apps],
  theme: {
    ...theme,
  },
  plugins: [...pluginsStatic, ...pluginsToAdd],
};
