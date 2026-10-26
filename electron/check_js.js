const fs = require('fs');
const acorn = require('acorn');

['home.html', 'processes.html', 'applications.html', 'organizer.html'].forEach(file => {
  const code = fs.readFileSync('../frontend/views/' + file, 'utf8');
  let jsCode = "";
  let inScript = false;
  code.split('\n').forEach(line => {
    if (line.includes('<script>')) { inScript = true; return; }
    if (line.includes('</script>')) { inScript = false; return; }
    if (inScript) jsCode += line + '\n';
  });
  
  if (jsCode) {
    try {
      acorn.parse(jsCode, { ecmaVersion: 2020 });
      console.log(file + " parsed successfully.");
    } catch (e) {
      console.log(file + " syntax error:", e.message, "at line", Math.max(0, e.loc ? e.loc.line : 0));
    }
  }
});
