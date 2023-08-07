const fs = require("fs");
const path = require("path");

/**
 * Get all apps paths
 * @param {*} dir path to the directory
 * @returns array of paths to rendery
 */
const PluginsToAdd = (dir) => {
  if (fs.existsSync(dir) === false) {
    return [];
  }

  const dirs = fs.readdirSync(dir);
  const pathsToRender = [];
  dirs.forEach((childDir) => {
    if (childDir !== "__init__.py" && childDir !== "__pycache__") {
      pathsToRender.push(
        path.join(dir, childDir, "templates/**/*.{html,js}"),
        path.join(dir, childDir, "statics/**/*.js"),
        path.join(dir, childDir, "forms.py"),
        path.join(dir, childDir, "forms/**/*.py")
      );
    }
  });

  return pathsToRender;
};

module.exports = PluginsToAdd;
