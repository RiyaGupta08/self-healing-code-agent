import { motion } from 'motion/react';
import { Sparkles, Zap, ArrowRight } from 'lucide-react';
import imgContainer from "figma:asset/19ca50fc580ab226818961f02aa148e5f09ff338.png";

export function FigmaHeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-b from-[#0a0e1a] via-[#0f172a] to-[#0a0e1a]">
      {/* Enhanced animated background with grids */}
      <div className="absolute inset-0 opacity-30">
        <div 
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(rgba(0, 217, 255, 0.15) 1px, transparent 1px),
              linear-gradient(90deg, rgba(0, 217, 255, 0.15) 1px, transparent 1px)
            `,
            backgroundSize: '60px 60px',
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(rgba(139, 92, 246, 0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(139, 92, 246, 0.1) 1px, transparent 1px)
            `,
            backgroundSize: '60px 60px',
            backgroundPosition: '30px 30px',
          }}
        />
      </div>

      {/* Noise texture */}
      <div 
        className="absolute inset-0 opacity-10 pointer-events-none"
        style={{
          backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 400 400\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noiseFilter\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'1.2\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noiseFilter)\'/%3E%3C/svg%3E")',
        }}
      >
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <img alt="" className="absolute h-[150px] left-0 max-w-none top-0 w-[150px] opacity-10" src={imgContainer} />
        </div>
      </div>

      {/* Dramatic radial gradients */}
      <motion.div 
        className="absolute -top-64 left-0 w-[700px] h-[700px] rounded-full blur-[160px] opacity-25"
        style={{
          background: 'radial-gradient(circle, #00d9ff 0%, transparent 70%)',
        }}
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.25, 0.35, 0.25],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      
      <motion.div 
        className="absolute top-1/3 right-0 w-[650px] h-[650px] rounded-full blur-[150px] opacity-20"
        style={{
          background: 'radial-gradient(circle, #8b5cf6 0%, transparent 70%)',
        }}
        animate={{
          scale: [1, 1.3, 1],
          opacity: [0.2, 0.3, 0.2],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 1,
        }}
      />

      <motion.div 
        className="absolute bottom-0 left-1/3 w-[530px] h-[530px] rounded-full blur-[130px] opacity-20"
        style={{
          background: 'radial-gradient(circle, #06b6d4 0%, transparent 70%)',
        }}
        animate={{
          scale: [1, 1.15, 1],
          opacity: [0.2, 0.28, 0.2],
        }}
        transition={{
          duration: 9,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 2,
        }}
      />

      {/* Energy lines */}
      <svg className="absolute inset-0 w-full h-full opacity-40 pointer-events-none">
        <defs>
          <linearGradient id="heroLineGradient1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00d9ff" stopOpacity="0" />
            <stop offset="50%" stopColor="#00d9ff" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#00d9ff" stopOpacity="0" />
          </linearGradient>
          <linearGradient id="heroLineGradient2" x1="100%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0" />
            <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0" />
          </linearGradient>
        </defs>
        
        <line x1="0" y1="10%" x2="100%" y2="10%" stroke="url(#heroLineGradient1)" strokeWidth="2">
          <animate attributeName="y1" values="10%;40%;10%" dur="20s" repeatCount="indefinite" />
          <animate attributeName="y2" values="10%;40%;10%" dur="20s" repeatCount="indefinite" />
        </line>
        
        <line x1="0" y1="60%" x2="100%" y2="60%" stroke="url(#heroLineGradient2)" strokeWidth="2">
          <animate attributeName="y1" values="60%;85%;60%" dur="25s" repeatCount="indefinite" />
          <animate attributeName="y2" values="60%;85%;60%" dur="25s" repeatCount="indefinite" />
        </line>

        <line x1="20%" y1="0" x2="20%" y2="100%" stroke="url(#heroLineGradient1)" strokeWidth="1.5">
          <animate attributeName="x1" values="20%;70%;20%" dur="30s" repeatCount="indefinite" />
          <animate attributeName="x2" values="20%;70%;20%" dur="30s" repeatCount="indefinite" />
        </line>
      </svg>

      {/* Vignette */}
      <div 
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'radial-gradient(circle at center, transparent 0%, rgba(10, 14, 26, 0.8) 100%)',
        }}
      />

      {/* Top spotlight */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-5xl h-full">
        <div className="absolute inset-0 bg-gradient-to-b from-[#00d9ff]/20 via-transparent to-transparent blur-3xl" />
      </div>

      {/* Main content */}
      <div className="max-w-6xl mx-auto px-6 py-20 relative z-10">
        <div className="text-center">
          {/* Premium AI badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, type: 'spring' }}
            className="mb-10 inline-flex items-center gap-3 px-6 py-3 rounded-full border border-[#00d9ff]/40 bg-gradient-to-r from-[#00d9ff]/10 via-[#8b5cf6]/10 to-[#00d9ff]/10 backdrop-blur-md relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff]/20 via-[#8b5cf6]/20 to-[#00d9ff]/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
            >
              <Sparkles className="w-4 h-4 text-[#00d9ff]" />
            </motion.div>
            <span className="text-sm font-semibold text-[#00d9ff] relative tracking-wider" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              POWERED BY ADVANCED AI AGENTS
            </span>
            <div className="w-2 h-2 rounded-full bg-[#00d9ff] animate-pulse" />
          </motion.div>

          {/* Dramatic hero text */}
          <div className="mb-10 relative">
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.1 }}
              className="relative inline-block"
              style={{ fontFamily: 'Orbitron, sans-serif' }}
            >
              <span className="block text-6xl md:text-7xl lg:text-8xl xl:text-9xl font-black text-white mb-4 tracking-tighter">
                FIX YOUR CODE
              </span>
              
              <span className="block text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-black tracking-tighter relative">
                {/* Glow effect behind text */}
                <span className="absolute inset-0 bg-gradient-to-r from-[#00d9ff] via-[#8b5cf6] to-[#00d9ff] bg-clip-text text-transparent blur-2xl opacity-60">
                  AUTOMATICALLY
                </span>
                <span className="relative bg-gradient-to-r from-[#00d9ff] via-[#8b5cf6] to-[#00d9ff] bg-clip-text text-transparent animate-gradient" style={{ backgroundSize: '200% auto' }}>
                  AUTOMATICALLY
                </span>
              </span>

              {/* Decorative rotating circle */}
              <motion.div
                className="absolute -right-20 top-1/2 -translate-y-1/2 hidden xl:block"
                animate={{ 
                  rotate: [0, 360],
                  scale: [1, 1.1, 1],
                }}
                transition={{ 
                  rotate: { duration: 20, repeat: Infinity, ease: 'linear' },
                  scale: { duration: 2, repeat: Infinity, ease: 'easeInOut' },
                }}
              >
                <div className="w-24 h-24 rounded-full border-2 border-[#00d9ff]/30 flex items-center justify-center shadow-[0_0_30px_rgba(0,217,255,0.3)]">
                  <div className="w-16 h-16 rounded-full border-2 border-[#8b5cf6]/30 flex items-center justify-center">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#00d9ff] to-[#8b5cf6]" />
                  </div>
                </div>
              </motion.div>
            </motion.h1>

            {/* Accent line */}
            <motion.div
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ duration: 1, delay: 0.5 }}
              className="h-1 w-32 mx-auto mt-8 rounded-full bg-gradient-to-r from-transparent via-[#00d9ff] to-transparent"
            />
          </div>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="text-lg md:text-xl lg:text-2xl text-[#cbd5e1] max-w-4xl mx-auto mb-14 leading-relaxed px-4"
            style={{ fontFamily: 'Space Grotesk, sans-serif', fontWeight: 300 }}
          >
            Experience the power of <span className="text-[#00d9ff] font-semibold">agentic debugging</span>. 
            Our AI agent observes, reasons, plans, and executes fixes autonomously—then validates them in real-time.
          </motion.p>

          {/* CTA buttons with professional styling */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-16"
          >
            <button className="group relative px-12 py-5 rounded-xl overflow-hidden transition-all duration-300 hover:scale-105 shadow-[0_0_40px_rgba(0,217,255,0.3)]">
              {/* Animated gradient background */}
              <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff] via-[#06b6d4] to-[#00d9ff] animate-gradient" style={{ backgroundSize: '200% auto' }} />
              
              {/* Intense glow effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] opacity-0 group-hover:opacity-100 blur-2xl transition-opacity duration-500" />
              
              {/* Shine effect */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
                animate={{
                  x: ['-200%', '200%'],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  repeatDelay: 2,
                }}
              />
              
              <span className="relative flex items-center gap-3 text-[#0a0e1a] font-bold text-lg" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                <Zap className="w-6 h-6" fill="currentColor" />
                Start Fixing Now
                <motion.div
                  animate={{ x: [0, 5, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                >
                  <ArrowRight className="w-5 h-5" />
                </motion.div>
              </span>
            </button>
            
            <button className="group relative px-12 py-5 rounded-xl border-2 border-[#00d9ff]/40 backdrop-blur-sm bg-[#00d9ff]/5 text-[#00d9ff] font-bold text-lg transition-all duration-300 hover:bg-[#00d9ff]/15 hover:border-[#00d9ff]/60 hover:shadow-[0_0_30px_rgba(0,217,255,0.3)]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              <span className="relative flex items-center gap-2">
                Watch Demo
                <div className="w-2 h-2 rounded-full bg-[#00d9ff] animate-pulse" />
              </span>
            </button>
          </motion.div>

          {/* Professional stat cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {[
              { value: '99.9', label: 'Success Rate %' },
              { value: '1.8', label: 'Avg Fix Time (s)' },
              { value: '500K+', label: 'Bugs Fixed' },
            ].map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 40, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ 
                  duration: 0.6, 
                  delay: 0.5 + index * 0.1,
                  type: 'spring',
                }}
                className="p-8 rounded-2xl border border-[#00d9ff]/20 bg-gradient-to-br from-[#0f172a]/90 to-[#1e293b]/60 backdrop-blur-xl relative overflow-hidden group hover:scale-105 transition-transform duration-300"
              >
                {/* Glow effect */}
                <div className="absolute -inset-0.5 bg-gradient-to-r from-[#00d9ff] via-[#8b5cf6] to-[#00d9ff] opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-500" />
                
                {/* Corner accent */}
                <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-[#00d9ff]/20 to-transparent rounded-bl-full" />
                
                <div className="relative z-10">
                  <div className="text-4xl md:text-5xl font-black text-[#00d9ff] mb-3 tracking-tight" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                    {stat.value}
                  </div>
                  <div className="text-sm text-[#94a3b8] uppercase tracking-wider" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                    {stat.label}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Enhanced scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1.2 }}
        className="absolute bottom-12 left-1/2 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 12, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          className="flex flex-col items-center gap-2"
        >
          <div className="text-xs text-[#64748b] uppercase tracking-widest mb-2" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Scroll
          </div>
          <div className="w-6 h-10 border-2 border-[#00d9ff]/40 rounded-full flex items-start justify-center p-2 relative overflow-hidden">
            <motion.div
              animate={{ y: [0, 16, 16], opacity: [1, 1, 0] }}
              transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
              className="w-1.5 h-1.5 bg-[#00d9ff] rounded-full"
            />
          </div>
        </motion.div>
      </motion.div>

      {/* Animation styles */}
      <style>{`
        @keyframes gradient {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        .animate-gradient {
          animation: gradient 3s ease infinite;
        }
      `}</style>
    </section>
  );
}
