const fs = require("fs");
const path = require("path");

/**
 * Get all apps paths
 * @param {*} dir path to the directory
 * @returns array of paths to rendery
 */
const AppsToRender = (dir) => {
  if (fs.existsSync(dir) === false) {
    return [];
  }

  const dirs = fs.readdirSync(dir);
  const pathsToRender = [];
  const pluginsToAdd = [];

  dirs.forEach((childDir) => {
    if (childDir !== "__init__.py" && childDir !== "__pycache__") {
      const templatesDir = path.join(dir, childDir, "templates");

      if (
        fs.existsSync(templatesDir) &&
        fs.statSync(templatesDir).isDirectory() &&
        fs.readdirSync(templatesDir).length > 0
      ) {
        pathsToRender.push(
          path.join(dir, childDir, "templates/**/*.{html,js}")
        );
      }

      const staticsDir = path.join(dir, childDir, "static");

      if (
        fs.existsSync(staticsDir) &&
        fs.statSync(staticsDir).isDirectory() &&
        fs.readdirSync(staticsDir).length > 0
      ) {
        pathsToRender.push(path.join(dir, childDir, "static/**/*.js"));
      }

      const formsFile = path.join(dir, childDir, "forms.py");

      if (fs.existsSync(formsFile)) {
        pathsToRender.push(formsFile);
      }

      const formsDir = path.join(dir, childDir, "forms");

      if (
        fs.existsSync(formsDir) &&
        fs.statSync(formsDir).isDirectory() &&
        fs.readdirSync(formsDir).length > 0
      ) {
        pathsToRender.push(path.join(dir, childDir, "forms/**/*.py"));
      }

      const tailwindPluginsDir = path.join(dir, childDir, "tailwind_plugins");

      if (
        fs.existsSync(tailwindPluginsDir) &&
        fs.statSync(tailwindPluginsDir).isDirectory() &&
        fs.readdirSync(tailwindPluginsDir).length > 0
      ) {
        // pathsToRender.push(
        //   path.join(dir, childDir, "tailwind_plugins/**/*.py")
        // );
        fs.readdirSync(tailwindPluginsDir).forEach((plugin) => {
          pluginsToAdd.push("../../" + path.join(tailwindPluginsDir, plugin));
        });
      }
    }
  });

  return [pathsToRender, pluginsToAdd];
};

module.exports = AppsToRender;
