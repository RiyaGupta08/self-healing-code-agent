import { motion } from 'motion/react';
import { ArrowRight, XCircle, CheckCircle2 } from 'lucide-react';

const beforeCode = `def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result

# Bug: Doesn't handle None values
output = process_data([1, 2, None, 4])`;

const afterCode = `def process_data(data):
    result = []
    for item in data:
        if item is not None:
            result.append(item * 2)
    return result

# Fixed: Now handles None values safely
output = process_data([1, 2, None, 4])`;

export function DemoComparison() {
  return (
    <section className="relative px-6 py-20">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4" style={{ fontFamily: 'Orbitron, sans-serif' }}>
            See The Difference
          </h2>
          <p className="text-lg text-[#94a3b8] max-w-2xl mx-auto" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Watch how our AI transforms buggy code into production-ready solutions
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-[1fr_auto_1fr] gap-8 items-start">
          {/* Before */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="relative"
          >
            {/* Label */}
            <div className="flex items-center gap-2 mb-4">
              <XCircle className="w-5 h-5 text-[#ef4444]" />
              <span className="text-lg font-semibold text-white" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Before
              </span>
              <span className="ml-auto px-3 py-1 rounded-full bg-[#ef4444]/20 text-[#ef4444] text-xs font-semibold">
                Has Bugs
              </span>
            </div>

            {/* Code panel */}
            <div className="rounded-xl border border-[#ef4444]/30 bg-gradient-to-br from-[#0f172a]/90 to-[#1e293b]/60 backdrop-blur-md overflow-hidden">
              {/* Header */}
              <div className="flex items-center justify-between px-4 py-3 border-b border-[#ef4444]/20 bg-[#0a0e1a]/50">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-[#ef4444]" />
                  <div className="w-3 h-3 rounded-full bg-[#eab308]" />
                  <div className="w-3 h-3 rounded-full bg-[#64748b]" />
                </div>
                <span className="text-xs text-[#64748b]">buggy.py</span>
              </div>

              {/* Code */}
              <div className="p-6 font-mono text-sm">
                <pre className="text-[#e4e8f0]">
                  {beforeCode.split('\n').map((line, index) => (
                    <div
                      key={index}
                      className={`flex gap-4 ${
                        index === 6 ? 'bg-[#ef4444]/10 border-l-2 border-[#ef4444] pl-4' : ''
                      }`}
                    >
                      <span className="text-[#475569] select-none w-6 text-right">
                        {index + 1}
                      </span>
                      <span>{line || ' '}</span>
                    </div>
                  ))}
                </pre>
              </div>

              {/* Error indicator */}
              <div className="px-6 pb-6">
                <div className="p-3 rounded-lg bg-[#ef4444]/10 border border-[#ef4444]/30 flex items-start gap-3">
                  <XCircle className="w-4 h-4 text-[#ef4444] mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-[#ef4444] mb-1">TypeError</p>
                    <p className="text-xs text-[#94a3b8]">
                      unsupported operand type(s) for *: 'NoneType' and 'int'
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Arrow */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="hidden lg:flex items-center justify-center"
          >
            <div className="relative">
              <motion.div
                animate={{ x: [0, 10, 0] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="w-12 h-12 rounded-full bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] flex items-center justify-center"
                style={{ boxShadow: '0 0 30px rgba(0, 217, 255, 0.5)' }}
              >
                <ArrowRight className="w-6 h-6 text-[#0a0e1a]" />
              </motion.div>
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] blur-xl opacity-50 animate-pulse" />
            </div>
          </motion.div>

          {/* Mobile arrow */}
          <div className="lg:hidden flex justify-center">
            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="w-12 h-12 rounded-full bg-gradient-to-r from-[#00d9ff] to-[#06b6d4] flex items-center justify-center rotate-90"
              style={{ boxShadow: '0 0 30px rgba(0, 217, 255, 0.5)' }}
            >
              <ArrowRight className="w-6 h-6 text-[#0a0e1a]" />
            </motion.div>
          </div>

          {/* After */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="relative"
          >
            {/* Label */}
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle2 className="w-5 h-5 text-[#22c55e]" />
              <span className="text-lg font-semibold text-white" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                After
              </span>
              <span className="ml-auto px-3 py-1 rounded-full bg-[#22c55e]/20 text-[#22c55e] text-xs font-semibold">
                Fixed
              </span>
            </div>

            {/* Code panel */}
            <div className="rounded-xl border border-[#22c55e]/30 bg-gradient-to-br from-[#0f172a]/90 to-[#1e293b]/60 backdrop-blur-md overflow-hidden">
              {/* Header */}
              <div className="flex items-center justify-between px-4 py-3 border-b border-[#22c55e]/20 bg-[#0a0e1a]/50">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-[#64748b]" />
                  <div className="w-3 h-3 rounded-full bg-[#64748b]" />
                  <div className="w-3 h-3 rounded-full bg-[#22c55e]" />
                </div>
                <span className="text-xs text-[#64748b]">fixed.py</span>
              </div>

              {/* Code */}
              <div className="p-6 font-mono text-sm">
                <pre className="text-[#e4e8f0]">
                  {afterCode.split('\n').map((line, index) => (
                    <div
                      key={index}
                      className={`flex gap-4 ${
                        index === 3 || index === 4
                          ? 'bg-[#22c55e]/10 border-l-2 border-[#22c55e] pl-4'
                          : ''
                      }`}
                    >
                      <span className="text-[#475569] select-none w-6 text-right">
                        {index + 1}
                      </span>
                      <span>{line || ' '}</span>
                    </div>
                  ))}
                </pre>
              </div>

              {/* Success indicator */}
              <div className="px-6 pb-6">
                <div className="p-3 rounded-lg bg-[#22c55e]/10 border border-[#22c55e]/30 flex items-start gap-3">
                  <CheckCircle2 className="w-4 h-4 text-[#22c55e] mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-[#22c55e] mb-1">All Tests Passed</p>
                    <p className="text-xs text-[#94a3b8]">
                      Code now handles None values gracefully • 100% test coverage
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {[
            { value: '1.8s', label: 'Time to Fix' },
            { value: '3 lines', label: 'Code Changed' },
            { value: '100%', label: 'Test Success' },
          ].map((stat, index) => (
            <div
              key={index}
              className="p-6 rounded-xl border border-[#00d9ff]/20 bg-gradient-to-br from-[#0f172a]/80 to-[#1e293b]/40 backdrop-blur-md text-center"
            >
              <div className="text-3xl font-bold text-[#00d9ff] mb-2" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                {stat.value}
              </div>
              <div className="text-sm text-[#94a3b8]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {stat.label}
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
