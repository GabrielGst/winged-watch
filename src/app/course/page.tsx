"use client";

import MapWGS84 from "@/components/MapWGS84";
import Header from "@/components/Header";

export default async function Home() {
  
  function handleClick(address: string) {
    fetch(address)
    console.log(address)
  }

  function processCourse() {
    handleClick("http://localhost:3000/api/course")
  }

  function getHealthStatus() {
    fetch("http://localhost:3000/api/healthchecker")
    .then(response => response.json())
    .then(data => console.log(data))
  }

  return (
    <div className="grid grid-rows-[20px_1fr_10px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      

      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={getHealthStatus}>Compute course !</button>
      <MapWGS84 /> 
    </div>
  );
}
