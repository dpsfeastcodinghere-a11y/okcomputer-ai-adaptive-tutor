// Quick fix script to remove orphaned database content from learning.html
// Run this to clean up the file

const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'learning.html');
let content = fs.readFileSync(filePath, 'utf8');

// Find the start of the orphaned content (after the fallback initialization)
const startMarker = 'if (!window.CONTENT_DATABASE) window.CONTENT_DATABASE = {};';
const endMarker = '// Learning Session Management\n        class LearningSession {';

const startIndex = content.indexOf(startMarker);
const endIndex = content.indexOf(endMarker);

if (startIndex !== -1 && endIndex !== -1) {
    const before = content.substring(0, startIndex + startMarker.length);
    const after = content.substring(endIndex);

    content = before + '\n\n        ' + after;

    fs.writeFileSync(filePath, content, 'utf8');
    console.log('✅ Successfully cleaned up learning.html');
    console.log('Removed orphaned database content');
} else {
    console.log('❌ Could not find markers in file');
}
