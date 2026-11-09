import React,{useMemo} from 'react';
import * as THREE from 'three';

// Local procedural replacement for the NOVA GLB, using the same metre coordinates.
export default function NovaHouse(){
 const gable=useMemo(()=>{const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute([-2,2.65,0,2,2.65,0,0,3.55,0],3));g.computeVertexNormals();return g},[]);
 const angle=Math.atan2(.96,2.12),slope=Math.hypot(2.12,.96);
 const box=(key,p,s,color,rotation)=> <mesh key={key} position={p} rotation={rotation} castShadow receiveShadow><boxGeometry args={s}/><meshStandardMaterial color={color} roughness={.66} metalness={color==='#33383c'?.55:0}/></mesh>;
 return <group>
  {box('floor',[0,.22,0],[4,.16,3],'#927047')}
  {[-1,1].map(side=>box(`side-${side}`,[side*1.92,1.48,-.18],[.18,2.35,2.64],'#d5c4a4'))}
  {box('rear',[0,1.48,-1.41],[3.82,2.36,.178],'#d5c4a4')}
  {[-1,1].flatMap(side=>Array.from({length:16},(_,i)=>box(`clad-${side}-${i}`,[side*2.01,1.48,-1.5+(i+.5)*3/16],[.035,2.36,.18],'#33383c')))}
  <mesh geometry={gable} position={[0,0,1.13]} castShadow><meshStandardMaterial color="#a58254" side={THREE.DoubleSide}/></mesh>
  <mesh geometry={gable} position={[0,0,-1.5]} castShadow><meshStandardMaterial color="#33383c" side={THREE.DoubleSide}/></mesh>
  {[-1,1].flatMap(side=>[0,1,2].map(i=>box(`front-${side}-${i}`,[side*(1.72+i*.105),1.47,1.48],[.1,2.4,.095],i%2?'#a58254':'#927047')))}
  {Array.from({length:4},(_,i)=>{const x=-1.54+(i+.5)*.77;return <group key={i}>
   <mesh position={[x,1.405,1.155]} castShadow><boxGeometry args={[.69,2.03,.025]}/><meshPhysicalMaterial color="#dae4df" transmission={.9} roughness={.1} thickness={.025} ior={1.45}/></mesh>
   {box(`frame-left-${i}`,[x-.358,1.405,1.175],[.054,2.15,.09],'#282c2e')}
   {box(`frame-right-${i}`,[x+.358,1.405,1.175],[.054,2.15,.09],'#282c2e')}
   {box(`frame-top-${i}`,[x,2.45,1.175],[.77,.06,.09],'#282c2e')}
   {box(`frame-bottom-${i}`,[x,.36,1.175],[.77,.06,.09],'#282c2e')}
  </group>})}
  {[-1,1].map(side=>box(`roof-${side}`,[side*1.06,3.125,0],[slope,.095,3.36],'#33383c',[0,0,-side*angle]))}
  {[-1,1].flatMap(side=>Array.from({length:12},(_,i)=>box(`seam-${side}-${i}`,[side*1.06,3.185,-1.65+i*.3],[slope,.035,.018],'#33383c',[0,0,-side*angle])))}
  {box('ridge',[0,3.68,0],[.14,.055,3.42],'#33383c')}
  {Array.from({length:32},(_,i)=>box(`porch-${i}`,[-1.94+i*.125,.31,1.32],[.118,.055,.37],'#a58254'))}
  {[-1.65,0,1.65].flatMap(x=>[-1.25,1.25].map(z=>box(`foot-${x}-${z}`,[x,.07,z],[.22,.14,.22],'#777c7b')))}
 </group>
}
