import { motion } from 'motion/react';
import { Menu, X } from 'lucide-react';
import { useState } from 'react';

export function ProfessionalNav() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.6, type: 'spring' }}
        className="fixed top-0 left-0 right-0 z-50 px-6 py-4 backdrop-blur-xl bg-[#0a0e1a]/80 border-b border-[#00d9ff]/10"
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <motion.div
            className="flex items-center gap-3 group cursor-pointer"
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.2 }}
          >
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#00d9ff] to-[#06b6d4] flex items-center justify-center shadow-lg shadow-[#00d9ff]/30 group-hover:shadow-[#00d9ff]/50 transition-shadow duration-300">
                <span className="text-[#0a0e1a] font-bold text-xl" style={{ fontFamily: 'Inter, sans-serif' }}>
                  S
                </span>
              </div>
              {/* Rotating ring decoration */}
              <motion.div
                className="absolute -inset-1 border-2 border-[#00d9ff]/30 rounded-xl"
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
              />
            </div>
            <span className="text-xl font-bold text-white" style={{ fontFamily: 'Orbitron, sans-serif' }}>
              Self-Healing Code
            </span>
          </motion.div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-10">
            {['Features', 'How It Works', 'Docs'].map((item, index) => (
              <motion.a
                key={item}
                href={`#${item.toLowerCase().replace(/ /g, '-')}`}
                className="relative text-sm text-[#94a3b8] hover:text-[#00d9ff] transition-colors group"
                style={{ fontFamily: 'Space Grotesk, sans-serif' }}
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
              >
                {item}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] group-hover:w-full transition-all duration-300" />
              </motion.a>
            ))}
            
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4, delay: 0.3 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="relative px-6 py-2.5 bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] rounded-lg text-[#0a0e1a] font-semibold text-sm overflow-hidden group"
              style={{ fontFamily: 'Space Grotesk, sans-serif' }}
            >
              {/* Shine effect */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
                animate={{
                  x: ['-200%', '200%'],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  repeatDelay: 1,
                }}
              />
              <span className="relative">Get Started</span>
              
              {/* Glow effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-300" />
            </motion.button>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden text-[#00d9ff] p-2"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </motion.nav>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="fixed top-20 left-0 right-0 z-40 md:hidden px-6 py-6 backdrop-blur-xl bg-[#0a0e1a]/95 border-b border-[#00d9ff]/10"
        >
          <div className="flex flex-col gap-4">
            {['Features', 'How It Works', 'Docs'].map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase().replace(/ /g, '-')}`}
                className="text-[#94a3b8] hover:text-[#00d9ff] transition-colors py-2 border-b border-[#00d9ff]/10"
                style={{ fontFamily: 'Space Grotesk, sans-serif' }}
                onClick={() => setMobileMenuOpen(false)}
              >
                {item}
              </a>
            ))}
            <button
              className="px-6 py-3 bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] rounded-lg text-[#0a0e1a] font-semibold text-sm mt-2"
              style={{ fontFamily: 'Space Grotesk, sans-serif' }}
            >
              Get Started
            </button>
          </div>
        </motion.div>
      )}
    </>
  );
}
