import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';

interface AnimatedCounterProps {
  value: string;
  label: string;
  duration?: number;
}

export function AnimatedCounter({ value, label, duration = 2000 }: AnimatedCounterProps) {
  const [displayValue, setDisplayValue] = useState('0');
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isVisible) {
          setIsVisible(true);
        }
      },
      { threshold: 0.3 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, [isVisible]);

  useEffect(() => {
    if (!isVisible) return;

    // Extract numeric part and suffix
    const match = value.match(/^([\d.]+)(.*)$/);
    if (!match) {
      setDisplayValue(value);
      return;
    }

    const [, numStr, suffix] = match;
    const targetNum = parseFloat(numStr);
    const startTime = Date.now();

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Easing function (ease out)
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = targetNum * eased;

      // Format based on original format
      let formatted: string;
      if (numStr.includes('.')) {
        formatted = current.toFixed(1);
      } else {
        formatted = Math.floor(current).toString();
      }

      setDisplayValue(formatted + suffix);

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    animate();
  }, [isVisible, value, duration]);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={isVisible ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6 }}
      className="p-6 rounded-xl border border-[#00d9ff]/20 bg-gradient-to-br from-[#0f172a]/80 to-[#1e293b]/40 backdrop-blur-md relative overflow-hidden group"
    >
      {/* Animated gradient border */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-[#00d9ff] via-[#8b5cf6] to-[#00d9ff] opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-500" />
      
      {/* Glow effect */}
      <div className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <div className="absolute inset-0 bg-gradient-to-br from-[#00d9ff]/10 to-transparent" />
      </div>

      <div className="relative z-10">
        <div className="text-4xl md:text-5xl font-bold text-[#00d9ff] mb-2 tracking-tight" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          {displayValue}
        </div>
        <div className="text-sm text-[#94a3b8] uppercase tracking-wider" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          {label}
        </div>
      </div>

      {/* Corner accent */}
      <div className="absolute top-0 right-0 w-16 h-16 bg-gradient-to-br from-[#00d9ff]/20 to-transparent rounded-bl-full" />
    </motion.div>
  );
}
