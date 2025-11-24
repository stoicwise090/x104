import React, { useState, useRef } from 'react';
import { Camera, Upload, ClipboardCheck, Activity, Award, AlertTriangle, ChevronRight, CheckCircle2, XCircle, MapPin, Dna, Info, Star, ShieldCheck, Quote } from 'lucide-react';

// Integrated BREED_RECOGNITION_PROMPT from the uploaded prompts.py
const BREED_RECOGNITION_PROMPT = `
### ROLE
You are an expert veterinarian and cattle/buffalo breed specialist with extensive knowledge of Indian indigenous and crossbred cattle and buffalo breeds.

### TASK
Your task is to analyze the provided image and identify the breed of cattle or buffalo shown.

### CONTEXT & LISTS
Common Indian Cattle Breeds to consider:
- Gir, Sahiwal, Red Sindhi, Tharparkar, Rathi, Hariana, Ongole, Krishna Valley, Amritmahal, Hallikar, Khillari, Dangi, Deoni, Nimari, Malvi, Mewati, Nagori, Kankrej, etc.

Common Indian Buffalo Breeds to consider:
- Murrah, Nili-Ravi, Bhadawari, Jaffarabadi, Mehsana, Surti, Nagpuri, Toda, Pandharpuri, etc.

### OUTPUT FORMAT
Analyze the image carefully considering body structure, coat color, horn shape, facial features, body size, and any distinctive breed markers.
Provide your analysis in the following structured Markdown format. DO NOT change the header titles:

## 🧬 Primary Breed Identification
* **Breed Name:** [The most likely breed name]
* **Species:** [Cattle or Buffalo]

## 🎯 Confidence Level
* **Level:** [High/Medium/Low]

## 📏 Key Physical Characteristics
[List the specific visual features that led to this identification, such as horn shape, forehead, coat color, etc.]

## 🔄 Alternative Possibilities
[If uncertain, mention 1-2 other possible breeds]

## 🌍 Breed Category & Origin
* **Category:** [Indigenous/Crossbred/Exotic]
* **Geographic Origin:** [Traditional region/state where this breed is commonly found]

## 📝 Reasoning
[Detailed reasoning for your identification based on the visual evidence.]
`;

export default function CattleEvaluator() {
  const [image, setImage] = useState(null);
  const [imageBase64, setImageBase64] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      processFile(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = (file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setImage(reader.result);
      const base64String = reader.result.split(',')[1];
      setImageBase64(base64String);
      setResult(null);
      setError(null);
    };
    reader.readAsDataURL(file);
  };

  const analyzeImage = async () => {
    if (!imageBase64) return;

    setLoading(true);
    setError(null);
    const apiKey = ""; // System will provide key

    try {
      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [
              {
                parts: [
                  { text: BREED_RECOGNITION_PROMPT },
                  {
                    inlineData: {
                      mimeType: "image/jpeg",
                      data: imageBase64,
                    },
                  },
                ],
              },
            ],
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error?.message || "Failed to analyze image");
      }

      const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
      if (text) {
        setResult(text);
      } else {
        throw new Error("No analysis received from the model.");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // --- NEW: Parsing Logic to split the Markdown into structured data ---
  const parseReport = (text) => {
    const sections = text.split(/##\s+/).filter(Boolean);
    const data = {
      breedName: "Unknown Breed",
      species: "Unknown",
      confidence: "Low",
      characteristics: [],
      alternatives: "",
      category: "Unknown",
      origin: "Unknown",
      reasoning: ""
    };

    sections.forEach(section => {
      const lines = section.split('\n');
      const title = lines[0].trim();
      const content = lines.slice(1).join('\n').trim();

      if (title.includes("Primary Breed Identification")) {
        const breedMatch = content.match(/\*\*Breed Name:\*\*\s*(.*)/);
        const speciesMatch = content.match(/\*\*Species:\*\*\s*(.*)/);
        if (breedMatch) data.breedName = breedMatch[1].trim();
        if (speciesMatch) data.species = speciesMatch[1].trim();
      } else if (title.includes("Confidence Level")) {
        const confMatch = content.match(/\*\*Level:\*\*\s*(.*)/);
        if (confMatch) data.confidence = confMatch[1].trim();
      } else if (title.includes("Key Physical Characteristics")) {
        // Clean up bullets and create array
        data.characteristics = content.split('\n')
          .filter(line => line.trim().startsWith('*') || line.trim().startsWith('-'))
          .map(line => line.replace(/^[\*\-]\s*/, '').trim());
        if (data.characteristics.length === 0) data.characteristics = [content];
      } else if (title.includes("Alternative Possibilities")) {
        data.alternatives = content;
      } else if (title.includes("Breed Category & Origin")) {
        const catMatch = content.match(/\*\*Category:\*\*\s*(.*)/);
        const originMatch = content.match(/\*\*Geographic Origin:\*\*\s*(.*)/);
        if (catMatch) data.category = catMatch[1].trim();
        if (originMatch) data.origin = originMatch[1].trim();
      } else if (title.includes("Reasoning")) {
        data.reasoning = content;
      }
    });

    return data;
  };

  const ReportDashboard = ({ text }) => {
    if (!text) return null;
    const data = parseReport(text);

    return (
      <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
        
        {/* 1. Hero Card: Breed Identity */}
        <div className="bg-gradient-to-r from-emerald-600 to-teal-700 rounded-2xl p-6 text-white shadow-lg relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-white/10 rounded-full blur-2xl"></div>
          <div className="relative z-10">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-emerald-100 text-sm font-medium tracking-wide uppercase mb-1">Identified Breed</p>
                <h2 className="text-3xl font-bold tracking-tight mb-2">{data.breedName}</h2>
                <div className="flex flex-wrap gap-2 mt-3">
                  <span className="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1">
                    <Dna className="w-3 h-3" /> {data.species}
                  </span>
                  <span className="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1">
                    <Award className="w-3 h-3" /> {data.category}
                  </span>
                </div>
              </div>
              <div className="bg-white/10 p-3 rounded-xl border border-white/20 backdrop-blur-md text-center min-w-[80px]">
                 <p className="text-xs text-emerald-100 mb-1">Confidence</p>
                 <div className="text-xl font-bold flex items-center justify-center gap-1">
                   {data.confidence === 'High' ? <CheckCircle2 className="w-5 h-5 text-green-300" /> : <AlertTriangle className="w-5 h-5 text-yellow-300" />}
                 </div>
                 <p className="text-xs font-medium mt-1">{data.confidence}</p>
              </div>
            </div>
          </div>
        </div>

        {/* 2. Key Stats Grid */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm flex items-start gap-3">
             <div className="bg-blue-50 p-2 rounded-lg text-blue-600 shrink-0">
               <MapPin className="w-5 h-5" />
             </div>
             <div>
               <p className="text-xs text-slate-500 font-medium uppercase">Origin</p>
               <p className="text-sm font-semibold text-slate-800 leading-tight mt-1">{data.origin}</p>
             </div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm flex items-start gap-3">
             <div className="bg-purple-50 p-2 rounded-lg text-purple-600 shrink-0">
               <Activity className="w-5 h-5" />
             </div>
             <div>
               <p className="text-xs text-slate-500 font-medium uppercase">Type</p>
               <p className="text-sm font-semibold text-slate-800 leading-tight mt-1">{data.category}</p>
             </div>
          </div>
        </div>

        {/* 3. Physical Characteristics */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="bg-slate-50 px-5 py-3 border-b border-slate-200 flex items-center gap-2">
            <Info className="w-4 h-4 text-slate-500" />
            <h3 className="font-semibold text-slate-700 text-sm">Key Physical Markers</h3>
          </div>
          <div className="p-5">
            <ul className="space-y-3">
              {data.characteristics.map((char, index) => (
                <li key={index} className="flex items-start gap-3 text-sm text-slate-600">
                  <span className="bg-emerald-100 text-emerald-600 rounded-full p-1 mt-0.5 shrink-0">
                    <CheckCircle2 className="w-3 h-3" />
                  </span>
                  <span>{char}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* 4. Expert Reasoning */}
        <div className="bg-amber-50/50 rounded-xl border border-amber-100/50 p-5 relative">
          <Quote className="w-8 h-8 text-amber-200 absolute top-4 right-4 opacity-50" />
          <h3 className="text-amber-800 font-semibold text-sm mb-3 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4" />
            Expert Reasoning
          </h3>
          <p className="text-slate-700 text-sm leading-relaxed italic relative z-10">
            "{data.reasoning.replace(/\[|\]/g, '')}"
          </p>
        </div>

        {/* 5. Alternatives (if any) */}
        {data.alternatives && data.alternatives.length > 10 && (
           <div className="px-4 py-3 bg-slate-100 rounded-lg text-xs text-slate-500 border border-slate-200">
             <span className="font-semibold text-slate-700 mr-2">Alternative Possibilities:</span>
             {data.alternatives.replace(/\[|\]/g, '')}
           </div>
        )}

      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* Header */}
      <header className="bg-slate-900 text-white shadow-lg sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-emerald-500 p-2 rounded-lg shadow-emerald-500/20 shadow-lg">
              <Dna className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">Rashtriya Gokul Mission</h1>
              <p className="text-slate-400 text-xs font-medium tracking-wide uppercase">AI Breed Analyst</p>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-2 text-xs font-medium bg-slate-800/50 px-3 py-1.5 rounded-full border border-slate-700 text-emerald-400">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
            <span>System Online</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left Column: Image Input (5 columns) */}
          <div className="lg:col-span-5 space-y-6">
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
               <div className="p-4 border-b border-slate-100 flex justify-between items-center">
                  <h2 className="font-semibold text-slate-800 flex items-center gap-2">
                    <Camera className="w-4 h-4 text-emerald-600" />
                    Specimen Photo
                  </h2>
                  {image && (
                     <button 
                       onClick={() => { setImage(null); setImageBase64(null); setResult(null); }}
                       className="text-xs text-red-500 hover:text-red-700 font-medium flex items-center gap-1"
                     >
                       <XCircle className="w-3 h-3" /> Clear
                     </button>
                  )}
               </div>
               
               <div className="p-4">
                  <div 
                    className={`relative border-2 border-dashed rounded-xl transition-all h-80 flex flex-col items-center justify-center text-center
                      ${image ? 'border-emerald-500 bg-emerald-50/10' : 'border-slate-300 hover:border-emerald-400 bg-slate-50 hover:bg-white'}
                    `}
                    onDragOver={(e) => e.preventDefault()}
                    onDrop={handleDrop}
                  >
                    {image ? (
                        <img 
                          src={image} 
                          alt="Animal preview" 
                          className="absolute inset-0 w-full h-full object-contain rounded-xl p-2" 
                        />
                    ) : (
                      <div 
                        className="cursor-pointer flex flex-col items-center gap-4 p-8 w-full h-full justify-center"
                        onClick={() => fileInputRef.current?.click()}
                      >
                        <div className="bg-white p-4 rounded-full shadow-sm border border-slate-100">
                          <Upload className="w-8 h-8 text-emerald-600" />
                        </div>
                        <div>
                          <p className="font-semibold text-slate-700">Upload Image</p>
                          <p className="text-xs text-slate-400 mt-1 max-w-[200px] mx-auto">Supports JPG, PNG. Ensure clear side profile for best results.</p>
                        </div>
                      </div>
                    )}
                    <input 
                      type="file" 
                      ref={fileInputRef}
                      className="hidden" 
                      accept="image/*"
                      onChange={handleImageUpload}
                    />
                  </div>

                  <button
                    onClick={analyzeImage}
                    disabled={!image || loading}
                    className={`w-full mt-4 py-3.5 px-6 rounded-xl font-semibold shadow-md transition-all flex items-center justify-center gap-2
                      ${!image 
                        ? 'bg-slate-100 text-slate-400 cursor-not-allowed shadow-none' 
                        : loading 
                          ? 'bg-slate-800 text-white cursor-wait' 
                          : 'bg-emerald-600 hover:bg-emerald-700 text-white hover:shadow-lg active:scale-[0.98]'}
                    `}
                  >
                    {loading ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white/30 border-t-white"></div>
                        <span>Analyzing Features...</span>
                      </>
                    ) : (
                      <>
                        <Activity className="w-4 h-4" />
                        <span>Identify Breed</span>
                      </>
                    )}
                  </button>

                  {error && (
                    <div className="mt-4 p-3 bg-red-50 border border-red-100 rounded-lg flex items-center gap-3">
                      <AlertTriangle className="w-4 h-4 text-red-600 shrink-0" />
                      <div className="text-xs text-red-700 font-medium">{error}</div>
                    </div>
                  )}
               </div>
            </div>
            
            {/* Quick Tips */}
            {!result && (
              <div className="bg-blue-50/50 rounded-xl p-4 border border-blue-100">
                <h4 className="text-xs font-bold text-blue-700 uppercase tracking-wide mb-2 flex items-center gap-2">
                  <Info className="w-3 h-3" />
                  Best Practices
                </h4>
                <ul className="space-y-2">
                  <li className="text-xs text-blue-800/70 flex items-start gap-2">
                    <span className="w-1 h-1 rounded-full bg-blue-400 mt-1.5"></span>
                    Ensure the animal's head and horns are clearly visible.
                  </li>
                  <li className="text-xs text-blue-800/70 flex items-start gap-2">
                    <span className="w-1 h-1 rounded-full bg-blue-400 mt-1.5"></span>
                    Side profile photos work best for body conformation.
                  </li>
                </ul>
              </div>
            )}
          </div>

          {/* Right Column: Report Dashboard (7 columns) */}
          <div className="lg:col-span-7">
            {result ? (
              <div className="relative">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
                    <ClipboardCheck className="w-5 h-5 text-emerald-600" />
                    Assessment Results
                  </h3>
                  <div className="flex gap-2">
                     <button 
                      className="text-xs text-slate-500 hover:text-emerald-700 font-medium flex items-center gap-1.5 bg-white border border-slate-200 px-3 py-1.5 rounded-lg shadow-sm transition-colors"
                      onClick={() => {
                          const blob = new Blob([result], { type: 'text/plain' });
                          const url = URL.createObjectURL(blob);
                          const a = document.createElement('a');
                          a.href = url;
                          a.download = 'Breed_Analysis_Report.txt';
                          a.click();
                      }}
                    >
                      <Upload className="w-3 h-3" />
                      Export
                    </button>
                  </div>
                </div>
                
                <ReportDashboard text={result} />

              </div>
            ) : (
              <div className="h-full min-h-[500px] border-2 border-dashed border-slate-200 rounded-2xl flex flex-col items-center justify-center text-slate-400 bg-slate-50/50 p-10">
                {!loading && (
                  <div className="text-center max-w-sm">
                    <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm border border-slate-100">
                       <Dna className="w-10 h-10 text-slate-300" />
                    </div>
                    <h3 className="text-lg font-semibold text-slate-700 mb-2">Waiting for Analysis</h3>
                    <p className="text-sm text-slate-500 leading-relaxed">
                      Upload a photo on the left to begin the automated breed identification process based on RGM standards.
                    </p>
                  </div>
                )}
                {loading && (
                  <div className="w-full max-w-md space-y-8">
                     <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center animate-pulse">
                           <Award className="w-6 h-6 text-emerald-500" />
                        </div>
                        <div className="flex-1 space-y-2">
                           <div className="h-2 bg-slate-200 rounded w-1/3 animate-pulse"></div>
                           <div className="h-2 bg-slate-100 rounded w-full animate-pulse"></div>
                        </div>
                     </div>
                     <div className="space-y-3 pl-16">
                        <div className="h-20 bg-white rounded-xl border border-slate-100 shadow-sm p-4 space-y-2">
                           <div className="h-2 bg-slate-100 rounded w-3/4 animate-pulse"></div>
                           <div className="h-2 bg-slate-100 rounded w-1/2 animate-pulse"></div>
                        </div>
                     </div>
                     <p className="text-center text-xs text-emerald-600 font-medium animate-pulse">Comparing with 30+ indigenous breed standards...</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
