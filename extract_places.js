const fs=require('fs');
const src=fs.readFileSync('script.js','utf8');
const m=src.match(/const PLACES=(\{[\s\S]*?\});\nconst CATEGORIES=/);
if(!m) throw new Error('no places');
const vm=require('vm');
const sandbox={};
vm.runInNewContext('PLACES='+m[1], sandbox);
fs.writeFileSync('/mnt/data/places.json', JSON.stringify(sandbox.PLACES,null,2));
