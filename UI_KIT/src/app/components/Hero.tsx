import { motion } from 'motion/react';
import { Sparkles, Zap, ArrowRight } from 'lucide-react';
import { AnimatedCounter } from './AnimatedCounter';

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 py-20 overflow-hidden">
      {/* Dramatic spotlight effect */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-4xl">
        <div className="absolute inset-0 bg-gradient-to-b from-[#00d9ff]/20 via-transparent to-transparent blur-3xl" />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="text-center">
          {/* Premium badge with animation */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, type: 'spring' }}
            className="mb-8 inline-flex items-center gap-2 px-5 py-2.5 rounded-full border border-[#00d9ff]/40 bg-gradient-to-r from-[#00d9ff]/10 via-[#8b5cf6]/10 to-[#00d9ff]/10 backdrop-blur-md relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff]/20 via-[#8b5cf6]/20 to-[#00d9ff]/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
            >
              <Sparkles className="w-4 h-4 text-[#00d9ff]" />
            </motion.div>
            <span className="text-sm font-semibold text-[#00d9ff] relative" style={{ fontFamily: 'Space Grotesk, sans-serif', letterSpacing: '0.05em' }}>
              POWERED BY ADVANCED AI AGENTS
            </span>
            <div className="w-2 h-2 rounded-full bg-[#00d9ff] animate-pulse" />
          </motion.div>

          {/* Dramatic hero text with asymmetric layout */}
          <div className="mb-8 relative">
            {/* Glowing text effect */}
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.1 }}
              className="relative inline-block"
              style={{ fontFamily: 'Orbitron, sans-serif' }}
            >
              <span className="block text-6xl md:text-8xl lg:text-9xl font-black text-white mb-4 tracking-tighter">
                FIX YOUR CODE
              </span>
              
              {/* Main headline with dramatic gradient */}
              <span className="block text-6xl md:text-8xl lg:text-9xl font-black tracking-tighter relative">
                <span className="absolute inset-0 bg-gradient-to-r from-[#00d9ff] via-[#8b5cf6] to-[#00d9ff] bg-clip-text text-transparent blur-lg opacity-60" style={{ filter: 'blur(20px)' }}>
                  AUTOMATICALLY
                </span>
                <span className="relative bg-gradient-to-r from-[#00d9ff] via-[#8b5cf6] to-[#00d9ff] bg-clip-text text-transparent animate-gradient" style={{ backgroundSize: '200% auto' }}>
                  AUTOMATICALLY
                </span>
              </span>

              {/* Decorative elements */}
              <motion.div
                className="absolute -right-16 top-1/2 -translate-y-1/2 hidden xl:block"
                animate={{ 
                  rotate: [0, 360],
                  scale: [1, 1.1, 1],
                }}
                transition={{ 
                  rotate: { duration: 20, repeat: Infinity, ease: 'linear' },
                  scale: { duration: 2, repeat: Infinity, ease: 'easeInOut' },
                }}
              >
                <div className="w-24 h-24 rounded-full border-2 border-[#00d9ff]/30 flex items-center justify-center">
                  <div className="w-16 h-16 rounded-full border-2 border-[#8b5cf6]/30 flex items-center justify-center">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#00d9ff] to-[#8b5cf6]" />
                  </div>
                </div>
              </motion.div>
            </motion.h1>

            {/* Floating accent line */}
            <motion.div
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ duration: 1, delay: 0.5 }}
              className="h-1 w-32 mx-auto mt-6 rounded-full bg-gradient-to-r from-transparent via-[#00d9ff] to-transparent"
            />
          </div>

          {/* Subtitle with better contrast */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="text-xl md:text-2xl text-[#cbd5e1] max-w-3xl mx-auto mb-12 leading-relaxed"
            style={{ fontFamily: 'Space Grotesk, sans-serif', fontWeight: 300 }}
          >
            Experience the power of <span className="text-[#00d9ff] font-semibold">agentic debugging</span>. 
            Our AI agent observes, reasons, plans, and executes fixes autonomously—then validates them in real-time.
          </motion.p>

          {/* Enhanced CTA buttons with glow */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-20"
          >
            <button className="group relative px-10 py-5 rounded-xl overflow-hidden transition-all duration-300 hover:scale-105">
              {/* Animated gradient background */}
              <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff] via-[#06b6d4] to-[#00d9ff] animate-gradient" style={{ backgroundSize: '200% auto' }} />
              
              {/* Glow effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] opacity-0 group-hover:opacity-100 blur-2xl transition-opacity duration-500" />
              
              {/* Button content */}
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
            
            <button className="group relative px-10 py-5 rounded-xl border-2 border-[#00d9ff]/40 backdrop-blur-sm bg-[#00d9ff]/5 text-[#00d9ff] font-bold text-lg transition-all duration-300 hover:bg-[#00d9ff]/15 hover:border-[#00d9ff]/60 hover:shadow-[0_0_30px_rgba(0,217,255,0.3)]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              <span className="relative flex items-center gap-2">
                Watch Demo
                <div className="w-2 h-2 rounded-full bg-[#00d9ff] animate-pulse" />
              </span>
            </button>
          </motion.div>

          {/* Animated counters with asymmetric layout */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            <AnimatedCounter value="99.9" label="Success Rate %" />
            <AnimatedCounter value="1.8" label="Avg Fix Time (s)" />
            <AnimatedCounter value="500000" label="Bugs Fixed +" />
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

      {/* Add custom animation for gradient */}
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