"use client";

import InputLabel from "@/components/InputLabel";

export default async function Home() {

  const formId: string = "trip-form";
  
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
      <form id={formId} className="grid grid-cols-1 gap-4">
        <InputLabel form={formId} type ="text" id="boat-name" placeholder="Boat name" />
        <InputLabel form={formId} type ="number" id="boat-draught" placeholder="Boat draught" />
        <InputLabel form={formId} type ="number" id="boat-sails" placeholder="Boat sails (square meters)" />
      </form>
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={getHealthStatus}>Compute course !</button> 
    </div>
  );
}
