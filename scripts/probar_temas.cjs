/* Pruebas del runtime real: migración, preferencias y cambios del sistema. Sin DOM externo. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const registry=JSON.parse(fs.readFileSync('temas.json','utf8'));
const source=fs.readFileSync('interacciones.js','utf8').split('  // Variante optativa:')[0]+'})();';
let assertions=0;
function equal(actual,expected){assert.deepEqual(actual,expected);assertions++;}
function load({initial,mode,style,dark=false,stored={},blocked=false}={}){
 const values=new Map(Object.entries(stored)),dataset={},listeners={},changes=[];
 const media={matches:dark,addEventListener:(name,fn)=>listeners.media=fn};
 const doc={documentElement:{dataset},querySelectorAll:()=>[],querySelector:selector=>{
  const value=selector.includes('nota-tema-inicial')?initial:selector.includes('nota-modo-inicial')?mode:style;return value?{content:value}:null;
 },addEventListener:(name,fn)=>listeners[name]=fn,dispatchEvent:event=>changes.push(event.detail)};
 const storage={getItem:key=>{if(blocked)throw Error('blocked');return values.get(key)||null},setItem:(key,value)=>{if(blocked)throw Error('blocked');values.set(key,value)}};
 const context={document:doc,window:{},localStorage:storage,matchMedia:()=>media,location:{pathname:'/fixture.html'},CustomEvent:class{constructor(name,props){Object.assign(this,{name},props)}}};
 vm.runInNewContext(source,context);
 return {api:context.window.NotaTemas,dataset,values,changes,changeSystem(value){media.matches=value;listeners.media()},choose(attr,value){listeners.change({target:{value,matches:selector=>selector===`[${attr}]`}})}};
}
let app=load();equal(app.dataset.themeFamily,'editorial');equal(app.dataset.themeMode,'system');equal(app.dataset.theme,'light');
for(const family of registry.familias){
 app.choose('data-elegir-tema',family.id);equal(app.dataset.themeMode,'system');
 app.changeSystem(true);equal(app.dataset.colorMode,'dark');equal(app.dataset.theme,typeof family.dark==='string'?family.dark:family.id+'-dark');
 app.choose('data-elegir-modo','light');app.changeSystem(false);app.changeSystem(true);equal(app.dataset.colorMode,'light');
 app.choose('data-elegir-modo','dark');app.changeSystem(false);equal(app.dataset.colorMode,'dark');
 app.choose('data-elegir-modo','system');equal(app.dataset.colorMode,'light');
}
for(const [alias,[family,mode]] of Object.entries(registry.alias_anteriores)){
 const old=load({stored:{'nota-tema':alias}});equal(old.dataset.themeFamily,family);equal(old.dataset.themeMode,mode);
 const scoped=load({initial:'editorial',mode:'system',stored:{'nota-tema:/fixture.html':alias}});equal(scoped.dataset.themeFamily,family);equal(scoped.dataset.themeMode,mode);
}
app=load({initial:'catppuccin',mode:'system',dark:true});app.api.set({family:'github',mode:'light'});
const restored=load({initial:'catppuccin',mode:'system',dark:true,stored:Object.fromEntries(app.values)});equal(restored.dataset.themeFamily,'github');equal(restored.dataset.themeMode,'light');
equal(restored.api.set({family:'invalid'}),false);equal(restored.api.set({mode:'invalid'}),false);equal(restored.dataset.themeFamily,'github');
const blocked=load({initial:'liftit',mode:'system',blocked:true});equal(blocked.api.set({mode:'dark'}),true);equal(blocked.dataset.theme,'liftit-dark');
const unscoped=load({stored:{'nota-apariencia-v2':'{"family":"sea","mode":"light"}','nota-tema':'dark'}});equal(unscoped.dataset.theme,'sea-light');
const corrupt=load({stored:{'nota-apariencia-v2':'broken'}});equal(corrupt.dataset.themeFamily,'editorial');
console.log(`${assertions} comprobaciones: 13 familias, modos independientes, cambio del SO, persistencia, alias y almacenamiento bloqueado.`);
