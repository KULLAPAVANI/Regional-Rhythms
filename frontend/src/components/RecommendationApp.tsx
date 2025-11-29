import React, { useState } from "react";
import { Mic } from "lucide-react";

const RecommendationApp: React.FC = () => {
  const [recording, setRecording] = useState(false);
  const [accent, setAccent] = useState<string | null>(null);
  const [menu, setMenu] = useState<string[]>([]);

  const accentMenus: Record<string, string[]> = {
    Telugu: ["Idly 🥞", "Dosa 🥙", "Pesarattu 🌿", "Biryani 🍛"],
    Tamil: ["Pongal 🍚", "Vada 🍩", "Dosa 🥞", "Sambar 🍲"],
    Malayalam: ["Appam 🥞", "Puttu 🍚", "Avial 🥗", "Fish Curry 🐟"],
    Hindi: ["Chole Bhature 🍲", "Rajma Chawal 🍚", "Paratha 🫓", "Paneer Tikka 🧀"],
    Kannada: ["Bisi Bele Bath 🍛", "Ragi Mudde 🍘", "Neer Dosa 🥞", "Mysore Pak 🍮"],
    Punjabi: ["Butter Chicken 🍗", "Amritsari Kulcha 🫓", "Lassi 🥛", "Chole 🍲"],
  };

  const startRecording = async () => {
    setRecording(true);
    setAccent(null);
    setMenu([]);

    // Simulate accent detection (replace with actual API later)
    setTimeout(() => {
      const accents = Object.keys(accentMenus);
      const randomAccent = accents[Math.floor(Math.random() * accents.length)];
      setAccent(randomAccent);
      setMenu(accentMenus[randomAccent]);
      setRecording(false);
    }, 4000);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-[#0f172a] text-white font-sans text-center px-4">
      <h1 className="text-2xl font-semibold mb-3 text-white">
        Cuisine Recommender Demo
      </h1>
      <p className="text-gray-300 mb-8 max-w-md">
        Click the button below and speak a short English phrase. We&apos;ll analyze your accent to recommend food.
      </p>

      <button
        onClick={startRecording}
        disabled={recording}
        className={`flex items-center gap-2 px-6 py-3 rounded-md font-semibold text-white transition ${
          recording
            ? "bg-gray-600 cursor-not-allowed"
            : "bg-[#149C8E] hover:bg-[#0d766b]"
        }`}
      >
        <Mic size={20} />
        {recording ? "Listening..." : "Start Accent Detection"}
      </button>

      {accent && (
        <div className="mt-10">
          <h2 className="text-xl font-semibold mb-2 text-teal-400">
            Detected Accent: {accent}-English
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-4">
            {menu.map((dish, index) => (
              <div
                key={index}
                className="bg-gray-800 hover:bg-gray-700 transition rounded-xl p-4 shadow-md text-lg"
              >
                {dish}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default RecommendationApp;
