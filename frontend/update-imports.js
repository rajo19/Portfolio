const fs = require('fs');
const path = require('path');

// Define the directory to process
const viewsDir = path.join(__dirname, 'src/views');

// Function to process a single file
function processFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let updated = false;

    // Update Vuetify component imports
    if (content.includes("from 'vuetify/lib/components")) {
      content = content.replace(
        /from 'vuetify\/lib\/components\/([^']+)'/g,
        "from 'vuetify/components/$1'"
      );
      updated = true;
    }

    // Update Vuetify directives
    if (content.includes("from 'vuetify/lib/directives")) {
      content = content.replace(
        /from 'vuetify\/lib\/directives\/([^']+)'/g,
        "from 'vuetify/directives/$1'"
      );
      updated = true;
    }

    // Save the file if it was updated
    if (updated) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`Updated: ${filePath}`);
    }
  } catch (err) {
    console.error(`Error processing ${filePath}:`, err);
  }
}

// Process all .vue files in the views directory
function processDirectory(directory) {
  const files = fs.readdirSync(directory);
  
  files.forEach(file => {
    const fullPath = path.join(directory, file);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      processDirectory(fullPath);
    } else if (file.endsWith('.vue') || file.endsWith('.js') || file.endsWith('.jsx') || file.endsWith('.ts') || file.endsWith('.tsx')) {
      processFile(fullPath);
    }
  });
}

// Start processing
console.log('Updating Vuetify imports...');
processDirectory(viewsDir);
processDirectory(path.join(__dirname, 'src')); // Also process other src files
console.log('Import updates complete!');
