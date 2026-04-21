import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Play, AlertCircle, CheckCircle2, Lightbulb, Loader2, Terminal, Sparkles, Copy } from 'lucide-react';

export function CodeInterface() {
  const [userCode, setUserCode] = useState('');
  const [isFixing, setIsFixing] = useState(false);
  const [isFixed, setIsFixed] = useState(false);
  const [fixedCode, setFixedCode] = useState('');
  const [errors, setErrors] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [reasoning, setReasoning] = useState('');
  const [executionResult, setExecutionResult] = useState(null);

  const handleFix = async () => {
    if (!userCode.trim()) {
      alert('Please paste some code first!');
      return;
    }

    setIsFixing(true);
    setIsFixed(false);
    setErrors([]);
    setSuggestions([]);
    setFixedCode('');
    setReasoning('');
    setExecutionResult(null);
    
    try {
      console.log('Sending code to backend:', userCode);
      
      const response = await fetch('http://127.0.0.1:8000/api/debug', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: userCode,
          language: 'python'
        })
      });

      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Full response data:', data);

      if (response.ok && data.success) {
        console.log('Fixed code received:', data.fixed_code);
        
        setFixedCode(data.fixed_code || 'Code fixed!');
        setIsFixed(true);
        
        if (data.error) {
          setErrors([{
            line: data.error.line_number || 'Unknown',
            type: data.error.error_type,
            message: data.error.message,
            severity: data.error.severity,
          }]);
        }
        
        if (data.fixes && data.fixes.length > 0) {
          setSuggestions(data.fixes.slice(0, 3).map((fix, idx) => ({
            rank: idx + 1,
            title: fix.description,
            description: fix.reasoning,
            confidence: Math.round(fix.confidence * 100),
            score: Math.round(fix.ranking_score),
          })));
        }
        
        if (data.execution_result) {
          setExecutionResult({
            success: data.execution_result.success,
            stdout: data.execution_result.stdout,
            stderr: data.execution_result.stderr,
          });
        }
        
        const confidence = data.confidence ? Math.round(data.confidence * 100) : 0;
        setReasoning(`✅ Fixed successfully! Confidence: ${confidence}% | Time: ${data.time_elapsed?.toFixed(2)}s`);
        
      } else if (response.ok && !data.success) {
        console.log('Error detected but could not fix');
        
        if (data.error) {
          setErrors([{
            line: data.error.line_number || 'Unknown',
            type: data.error.error_type,
            message: data.error.message,
            severity: data.error.severity,
          }]);
        }
        
        if (data.fixes && data.fixes.length > 0) {
          setSuggestions(data.fixes.slice(0, 3).map((fix, idx) => ({
            rank: idx + 1,
            title: fix.description,
            description: fix.reasoning,
            confidence: Math.round(fix.confidence * 100),
            score: Math.round(fix.ranking_score),
          })));
        }
        
        setReasoning(`⚠️ Error detected but could not auto-fix. Try one of the suggestions above.`);
        
      } else {
        console.log('Server error:', data);
        setErrors([{
          line: 0,
          type: 'Error',
          message: data.detail || data.message || 'Failed to debug code',
          severity: 'high',
        }]);
        setReasoning('❌ Could not process code');
      }
    } catch (error) {
      console.error('Fetch error:', error);
      setErrors([{
        line: 0,
        type: 'Connection Error',
        message: `Cannot connect to backend: ${error.message}. Make sure Python server is running on http://127.0.0.1:8000`,
        severity: 'high',
      }]);
      setReasoning('❌ Backend connection failed');
    } finally {
      setIsFixing(false);
    }
  };

  const handleReset = () => {
    setUserCode('');
    setIsFixed(false);
    setFixedCode('');
    setErrors([]);
    setSuggestions([]);
    setReasoning('');
    setExecutionResult(null);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('✅ Copied to clipboard!');
  };

  return (
    <section className="relative px-6 py-32">
      <div className="max-w-full mx-auto">
        {/* Section header */}
        <div className="mb-20 relative">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="flex items-start gap-6"
          >
            <div className="hidden lg:block">
              <div className="w-2 h-32 bg-gradient-to-b from-[#00d9ff] to-transparent rounded-full" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-4">
                <Terminal className="w-8 h-8 text-[#00d9ff]" />
                <span className="text-sm text-[#00d9ff] uppercase tracking-wider font-semibold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                  Live Demo
                </span>
              </div>
              <h2 className="text-5xl md:text-7xl font-black text-white mb-6 tracking-tight" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                INTELLIGENT
                <br />
                <span className="bg-gradient-to-r from-[#00d9ff] to-[#8b5cf6] bg-clip-text text-transparent">
                  CODE ANALYSIS
                </span>
              </h2>
              <p className="text-xl text-[#94a3b8] max-w-2xl" style={{ fontFamily: 'Space Grotesk, sans-serif', fontWeight: 300 }}>
                Paste your buggy code and watch our AI agent detect, analyze, and fix errors
              </p>
            </div>
          </motion.div>
        </div>

        {/* Main interface - FIXED RESPONSIVE GRID */}
        <div className="grid lg:grid-cols-[1fr_1fr] gap-8 items-start">
          
          {/* LEFT: Code Input Box */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="relative group h-full"
          >
            <div className="absolute -inset-0.5 bg-gradient-to-r from-[#00d9ff] via-[#8b5cf6] to-[#00d9ff] rounded-2xl opacity-20 group-hover:opacity-40 blur-xl transition-opacity duration-500" />
            
            <div className="relative rounded-2xl border border-[#00d9ff]/30 bg-gradient-to-br from-[#0f172a]/95 to-[#1e293b]/80 backdrop-blur-xl overflow-hidden shadow-2xl flex flex-col h-full">
              {/* Editor header */}
              <div className="flex items-center justify-between px-5 py-4 border-b border-[#00d9ff]/20 bg-gradient-to-r from-[#0a0e1a]/80 to-[#0f172a]/60 backdrop-blur-sm">
                <div className="flex items-center gap-3">
                  <div className="flex gap-2">
                    <div className="w-3.5 h-3.5 rounded-full bg-[#ef4444] shadow-lg shadow-[#ef4444]/50" />
                    <div className="w-3.5 h-3.5 rounded-full bg-[#eab308] shadow-lg shadow-[#eab308]/50" />
                    <div className="w-3.5 h-3.5 rounded-full bg-[#22c55e] shadow-lg shadow-[#22c55e]/50" />
                  </div>
                  <div className="h-4 w-px bg-[#00d9ff]/20 mx-2" />
                  <span className="text-sm text-[#94a3b8] font-mono">code_editor.py</span>
                </div>
                <div className="flex items-center gap-3">
                  <AnimatePresence>
                    {isFixed && (
                      <motion.div
                        initial={{ scale: 0, rotate: -180 }}
                        animate={{ scale: 1, rotate: 0 }}
                        exit={{ scale: 0 }}
                        className="flex items-center gap-2 px-3 py-1 rounded-full bg-[#22c55e]/20 border border-[#22c55e]/40"
                      >
                        <CheckCircle2 className="w-4 h-4 text-[#22c55e]" />
                        <span className="text-xs text-[#22c55e] font-semibold">FIXED ✅</span>
                      </motion.div>
                    )}
                  </AnimatePresence>
                  {isFixing && (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                    >
                      <Sparkles className="w-4 h-4 text-[#00d9ff]" />
                    </motion.div>
                  )}
                </div>
              </div>

              {/* Textarea - EDITABLE */}
              <textarea
                value={userCode}
                onChange={(e) => setUserCode(e.target.value)}
                placeholder="Paste your Python code here..."
                className="flex-1 p-8 font-mono text-sm bg-gradient-to-br from-[#0a0e1a]/50 to-transparent text-[#e4e8f0] placeholder-[#475569] border-none outline-none resize-none focus:ring-2 focus:ring-[#00d9ff]/50 transition-all"
                style={{
                  fontFamily: 'Monaco, Courier New, monospace',
                  minHeight: '300px',
                }}
              />

              {/* Bottom stats bar */}
              <div className="px-5 py-3 border-t border-[#00d9ff]/10 bg-[#0a0e1a]/60 backdrop-blur-sm flex items-center justify-between">
                <div className="flex items-center gap-4 text-xs text-[#64748b]">
                  <span>Python 3.11</span>
                  <div className="w-1 h-1 rounded-full bg-[#64748b]" />
                  <span>UTF-8</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-[#00d9ff]">
                  <div className="w-2 h-2 rounded-full bg-[#00d9ff] animate-pulse" />
                  <span>AI Active</span>
                </div>
              </div>
            </div>
          </motion.div>

          {/* RIGHT: Results Panels - Stack Vertically */}
          <div className="flex flex-col gap-6 h-full">
            
            {/* Detected Errors */}
            {errors.length > 0 && (
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="relative group"
              >
                <div className="absolute -inset-0.5 bg-gradient-to-r from-[#ef4444] to-[#dc2626] rounded-xl opacity-20 group-hover:opacity-40 blur-lg transition-opacity duration-500" />
                <div className="relative rounded-xl border border-[#ef4444]/30 bg-gradient-to-br from-[#0f172a]/95 to-[#1e293b]/80 backdrop-blur-xl p-6 shadow-xl">
                  <div className="flex items-center gap-3 mb-5">
                    <div className="p-2 rounded-lg bg-[#ef4444]/20 border border-[#ef4444]/40">
                      <AlertCircle className="w-5 h-5 text-[#ef4444]" />
                    </div>
                    <h3 className="font-bold text-white text-lg" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                      ❌ Error Detected
                    </h3>
                  </div>
                  <motion.div
                    key="errors"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-3"
                  >
                    {errors.map((error, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="p-4 rounded-lg bg-[#ef4444]/10 border border-[#ef4444]/30 hover:bg-[#ef4444]/15 transition-colors"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <span className="text-sm font-bold text-[#ef4444] font-mono">
                            {error.type}
                          </span>
                          {error.line && error.line !== 0 && (
                            <span className="text-xs text-[#94a3b8] font-mono">Line {error.line}</span>
                          )}
                        </div>
                        <p className="text-sm text-[#cbd5e1]">{error.message}</p>
                      </motion.div>
                    ))}
                  </motion.div>
                </div>
              </motion.div>
            )}

            {/* Suggested Fixes */}
            {suggestions.length > 0 && (
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.3 }}
                className="relative group"
              >
                <div className="absolute -inset-0.5 bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] rounded-xl opacity-20 group-hover:opacity-40 blur-lg transition-opacity duration-500" />
                <div className="relative rounded-xl border border-[#00d9ff]/30 bg-gradient-to-br from-[#0f172a]/95 to-[#1e293b]/80 backdrop-blur-xl p-6 shadow-xl">
                  <div className="flex items-center gap-3 mb-5">
                    <div className="p-2 rounded-lg bg-[#00d9ff]/20 border border-[#00d9ff]/40">
                      <Lightbulb className="w-5 h-5 text-[#00d9ff]" />
                    </div>
                    <h3 className="font-bold text-white text-lg" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                      💡 Fix Suggestions
                    </h3>
                  </div>
                  <div className="space-y-3">
                    {suggestions.map((suggestion, index) => (
                      <motion.div
                        key={suggestion.rank}
                        initial={{ opacity: 0, x: -10 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.1 }}
                        className="p-4 rounded-lg bg-[#00d9ff]/5 border border-[#00d9ff]/30 hover:bg-[#00d9ff]/10 hover:border-[#00d9ff]/50 transition-all cursor-pointer group/card relative overflow-hidden"
                      >
                        <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff]/10 to-transparent opacity-0 group-hover/card:opacity-100 transition-opacity" />
                        <div className="relative flex items-start justify-between mb-2">
                          <div className="flex items-center gap-3 flex-1">
                            <span className="flex items-center justify-center w-7 h-7 rounded-full bg-[#00d9ff]/30 text-[#00d9ff] text-xs font-bold border border-[#00d9ff]/50">
                              {suggestion.rank}
                            </span>
                            <span className="text-sm font-bold text-white">
                              {suggestion.title}
                            </span>
                          </div>
                          <div className="flex items-center gap-1 ml-2">
                            <span className="text-xs font-bold text-[#00d9ff]">{suggestion.confidence}%</span>
                          </div>
                        </div>
                        <p className="text-sm text-[#94a3b8] ml-10">{suggestion.description}</p>
                        <p className="text-xs text-[#64748b] ml-10 mt-1">Score: {suggestion.score}/100</p>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Analysis Result */}
            {reasoning && (
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="relative group"
              >
                <div className="absolute -inset-0.5 bg-gradient-to-r from-[#8b5cf6] to-[#a78bfa] rounded-xl opacity-20 group-hover:opacity-40 blur-lg transition-opacity duration-500" />
                <div className="relative rounded-xl border border-[#8b5cf6]/30 bg-gradient-to-br from-[#0f172a]/95 to-[#1e293b]/80 backdrop-blur-xl p-6 shadow-xl">
                  <h3 className="font-bold text-white mb-3 text-lg" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                    Analysis Status
                  </h3>
                  <p className="text-sm text-[#cbd5e1] leading-relaxed">
                    {reasoning}
                  </p>
                </div>
              </motion.div>
            )}

            {/* FIXED CODE - BIG AND PROMINENT */}
            {fixedCode && (
              <motion.div
                initial={{ opacity: 0, x: 30, scale: 0.95 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                transition={{ duration: 0.6 }}
                className="relative group"
              >
                <div className="absolute -inset-0.5 bg-gradient-to-r from-[#22c55e] via-[#16a34a] to-[#22c55e] rounded-2xl opacity-30 group-hover:opacity-50 blur-xl transition-opacity duration-500 animate-pulse" />
                <div className="relative rounded-2xl border border-[#22c55e]/50 bg-gradient-to-br from-[#0f172a]/95 to-[#1e293b]/80 backdrop-blur-xl p-8 shadow-2xl">
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                      <CheckCircle2 className="w-8 h-8 text-[#22c55e]" />
                      <h3 className="font-black text-2xl text-[#22c55e]" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                        ✅ FIXED CODE
                      </h3>
                    </div>
                    <button
                      onClick={() => copyToClipboard(fixedCode)}
                      className="flex items-center gap-2 px-4 py-2 bg-[#22c55e]/20 hover:bg-[#22c55e]/30 border border-[#22c55e]/50 rounded-lg transition-all text-[#22c55e] font-semibold"
                      title="Copy to clipboard"
                    >
                      <Copy className="w-5 h-5" />
                      Copy Code
                    </button>
                  </div>
                  
                  <pre className="bg-[#0a0e1a] p-6 rounded-lg text-[#22c55e] text-sm overflow-x-auto font-mono border border-[#22c55e]/20 shadow-inner">
                    <code>{fixedCode}</code>
                  </pre>

                  {executionResult && (
                    <div className="mt-4 p-4 rounded-lg bg-[#22c55e]/10 border border-[#22c55e]/30">
                      <p className="text-xs text-[#94a3b8] mb-2">Execution Result:</p>
                      <p className="text-sm text-[#22c55e]">
                        {executionResult.success ? '✅ Code runs successfully!' : '⚠️ Code has execution issues'}
                      </p>
                      {executionResult.stdout && (
                        <p className="text-xs text-[#cbd5e1] mt-2">Output: {executionResult.stdout}</p>
                      )}
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </div>
        </div>

        {/* Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="mt-16 flex justify-center gap-6 flex-wrap"
        >
          <button
            onClick={handleFix}
            disabled={isFixing || !userCode.trim()}
            className="group relative px-12 py-6 rounded-2xl overflow-hidden transition-all duration-500 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff] via-[#06b6d4] to-[#00d9ff]" style={{ backgroundSize: '200% auto' }} />
            <div 
              className="absolute inset-0 bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] opacity-0 group-hover:opacity-100 blur-3xl transition-opacity duration-500"
              style={{ filter: 'blur(40px)' }}
            />
            
            <span className="relative flex items-center gap-4 text-[#0a0e1a] font-black text-xl tracking-tight" style={{ fontFamily: 'Orbitron, sans-serif' }}>
              {isFixing ? (
                <>
                  <Loader2 className="w-7 h-7 animate-spin" />
                  ANALYZING...
                </>
              ) : (
                <>
                  <Play className="w-7 h-7" fill="currentColor" />
                  FIX MY CODE
                </>
              )}
            </span>
          </button>

          {(userCode || isFixed) && (
            <button
              onClick={handleReset}
              className="px-8 py-6 rounded-2xl bg-[#8b5cf6]/20 border border-[#8b5cf6]/50 text-white font-bold hover:bg-[#8b5cf6]/30 transition-all text-lg"
            >
              Reset
            </button>
          )}
        </motion.div>
      </div>
    </section>
  );
}
