import { useState, useEffect } from 'react'
import { 
  Shield, Lock, Globe, Search, FileCode, Github, 
  Terminal, Copy, Check, AlertTriangle, ArrowLeft,
  RefreshCw, Eye, EyeOff, Zap, Activity, Key,
  Server, Code, Fingerprint, ChevronRight, Sparkles
} from 'lucide-react'

// Tool registry with enhanced metadata
const tools = [
  {
    id: 'crypto',
    name: 'Cryptography Toolkit',
    shortName: 'Crypto',
    description: 'Enterprise-grade encryption utilities featuring SHA-256, AES-256-GCM, and RSA-2048',
    icon: Lock,
    color: '#00ff88',
    gradient: 'from-emerald-500/20 to-emerald-600/5'
  },
  {
    id: 'password',
    name: 'Password Security',
    shortName: 'Password',
    description: 'Advanced password analysis with zxcvbn scoring and bcrypt hashing',
    icon: Key,
    color: '#00d4ff',
    gradient: 'from-cyan-500/20 to-cyan-600/5'
  },
  {
    id: 'portscan',
    name: 'Network Scanner',
    shortName: 'Network',
    description: 'High-performance multi-threaded TCP port scanner with service detection',
    icon: Globe,
    color: '#ffa502',
    gradient: 'from-amber-500/20 to-amber-600/5'
  },
  {
    id: 'secrets',
    name: 'Secret Detector',
    shortName: 'Secrets',
    description: 'Automated detection of API keys, credentials, and sensitive tokens',
    icon: Search,
    color: '#ff4757',
    gradient: 'from-red-500/20 to-red-600/5'
  },
  {
    id: 'webtech',
    name: 'Tech Detector',
    shortName: 'Web Tech',
    description: 'Intelligent fingerprinting of web technologies and frameworks',
    icon: Code,
    color: '#a55eea',
    gradient: 'from-purple-500/20 to-purple-600/5'
  },
  {
    id: 'scorecard',
    name: 'Security Scorecard',
    shortName: 'Scorecard',
    description: 'Comprehensive GitHub repository security posture analysis',
    icon: Activity,
    color: '#7bed9f',
    gradient: 'from-green-500/20 to-green-600/5'
  },
  {
    id: 'packets',
    name: 'Packet Analyzer',
    shortName: 'Packets',
    description: 'Real-time network packet capture with SYN scan detection and HTTP analysis',
    icon: Activity,
    color: '#ff6b6b',
    gradient: 'from-red-500/20 to-pink-500/5'
  }
]


// Copy button with animation
function CopyButton({ text }) {
  const [copied, setCopied] = useState(false)
  
  const copy = async () => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }
  
  return (
    <button 
      onClick={copy}
      className="flex items-center gap-1.5 px-2 py-1 rounded-md bg-white/5 hover:bg-white/10 transition-colors text-xs font-medium"
      style={{ color: 'var(--color-primary)' }}
    >
      {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
      {copied ? 'Copied' : 'Copy'}
    </button>
  )
}

// Animated loading spinner
function LoadingSpinner() {
  return (
    <div className="flex items-center gap-2">
      <RefreshCw className="w-4 h-4 animate-spin" style={{ color: 'var(--color-primary)' }} />
      <span className="text-sm" style={{ color: 'var(--color-text-muted)' }}>Processing...</span>
    </div>
  )
}

// CRYPTO TOOLKIT COMPONENT
function CryptoToolkit() {
  const [mode, setMode] = useState('hash')
  const [input, setInput] = useState('')
  const [key, setKey] = useState('')
  const [output, setOutput] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleHash = async () => {
    if (!input) return
    setLoading(true)
    setError(null)
    
    try {
      const res = await fetch('/api/hash', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input })
      })
      setOutput(await res.json())
    } catch (err) {
      setError('Failed to generate hash')
    }
    setLoading(false)
  }

  const handleAESEncrypt = async () => {
    if (!input) return
    setLoading(true)
    setError(null)
    
    try {
      const res = await fetch('/api/aes/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plaintext: input, key: key || null })
      })
      const data = await res.json()
      setOutput(data)
      if (data.key) setKey(data.key)
    } catch (err) {
      setError('Encryption failed')
    }
    setLoading(false)
  }

  const handleAESDecrypt = async () => {
    if (!input || !key) return
    setLoading(true)
    setError(null)
    
    try {
      const res = await fetch('/api/aes/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ciphertext: input, key })
      })
      const data = await res.json()
      if (data.success) {
        setOutput({ plaintext: data.plaintext, mode: 'decrypt' })
      } else {
        setError('Decryption failed - invalid key or corrupted data')
      }
    } catch (err) {
      setError('Decryption failed')
    }
    setLoading(false)
  }

  const handleRSAGenerate = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const res = await fetch('/api/rsa/generate', { method: 'POST' })
      setOutput(await res.json())
    } catch (err) {
      setError('Key generation failed')
    }
    setLoading(false)
  }

  const handleRSAEncrypt = async () => {
    if (!input || !key) return
    setLoading(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('message', input)
      formData.append('public_key', key)
      
      const res = await fetch('/api/rsa/encrypt', { method: 'POST', body: formData })
      setOutput(await res.json())
    } catch (err) {
      setError('RSA encryption failed')
    }
    setLoading(false)
  }

  const handleRSADecrypt = async () => {
    if (!input || !key) return
    setLoading(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('ciphertext', input)
      formData.append('private_key', key)
      
      const res = await fetch('/api/rsa/decrypt', { method: 'POST', body: formData })
      setOutput(await res.json())
    } catch (err) {
      setError('RSA decryption failed')
    }
    setLoading(false)
  }

  const modes = [
    { id: 'hash', label: 'SHA-256 Hash', icon: Fingerprint },
    { id: 'aes', label: 'AES-256-GCM', icon: Shield },
    { id: 'rsa', label: 'RSA-2048', icon: Key }
  ]

  return (
    <div className="space-y-6">
      {/* Mode selector */}
      <div className="flex gap-2 p-1 rounded-xl bg-white/5">
        {modes.map(m => {
          const Icon = m.icon
          return (
            <button
              key={m.id}
              onClick={() => { setMode(m.id); setOutput(null); setError(null); setKey(''); }}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-lg font-medium text-sm transition-all duration-200 ${
                mode === m.id 
                  ? 'bg-emerald-500 text-black shadow-lg shadow-emerald-500/25' 
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
            >
              <Icon className="w-4 h-4" />
              {m.label}
            </button>
          )
        })}
      </div>

      {/* Hash Mode */}
      {mode === 'hash' && (
        <div className="space-y-4 fade-in">
          <div className="relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter text to generate SHA-256 hash..."
              className="input-field h-32 resize-none"
            />
            <div className="absolute bottom-3 right-3 text-xs text-gray-500">
              {input.length} chars
            </div>
          </div>
          
          <button 
            onClick={handleHash} 
            disabled={loading || !input}
            className="btn-primary w-full flex items-center justify-center gap-2"
          >
            {loading ? <LoadingSpinner /> : (
              <>
                <Fingerprint className="w-4 h-4" />
                Generate Hash
              </>
            )}
          </button>
          
          {output?.hash && (
            <div className="result-card">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-semibold text-emerald-400 flex items-center gap-2">
                  <Check className="w-4 h-4" />
                  SHA-256 Hash Generated
                </span>
                <CopyButton text={output.hash} />
              </div>
              <div className="p-3 rounded-lg bg-black/30 break-all text-sm font-mono text-gray-300 border border-white/5">
                {output.hash}
              </div>
              <div className="mt-2 text-xs text-gray-500">
                Length: {output.length} characters • Algorithm: SHA-256
              </div>
            </div>
          )}
        </div>
      )}

      {/* AES Mode */}
      {mode === 'aes' && (
        <div className="space-y-4 fade-in">
          <div className="relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter text to encrypt or decrypt..."
              className="input-field h-28 resize-none"
            />
          </div>
          
          <div className="relative">
            <input
              type="text"
              value={key}
              onChange={(e) => setKey(e.target.value)}
              placeholder="Encryption key (hex) - leave empty to auto-generate"
              className="input-field pr-10"
            />
            <Key className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-600" />
          </div>
          
          <div className="grid grid-cols-2 gap-3">
            <button 
              onClick={handleAESEncrypt} 
              disabled={loading || !input}
              className="btn-primary flex items-center justify-center gap-2"
            >
              <Lock className="w-4 h-4" />
              Encrypt
            </button>
            <button 
              onClick={handleAESDecrypt} 
              disabled={loading || !input || !key}
              className="btn-secondary flex items-center justify-center gap-2"
            >
              <UnlockIcon className="w-4 h-4" />
              Decrypt
            </button>
          </div>
          
          {output?.ciphertext && (
            <div className="result-card border-emerald-500/20">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-semibold text-emerald-400 flex items-center gap-2">
                  <Shield className="w-4 h-4" />
                  Encrypted with AES-256-GCM
                </span>
                <CopyButton text={output.ciphertext} />
              </div>
              <div className="p-3 rounded-lg bg-black/30 break-all text-xs font-mono text-gray-300 border border-white/5 max-h-32 overflow-y-auto">
                {output.ciphertext}
              </div>
              {output.key && (
                <div className="mt-3 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-semibold text-amber-400 flex items-center gap-1">
                      <AlertTriangle className="w-3 h-3" />
                      Save this key securely
                    </span>
                    <CopyButton text={output.key} />
                  </div>
                  <div className="text-xs font-mono text-amber-300/70 break-all">
                    {output.key}
                  </div>
                </div>
              )}
            </div>
          )}
          
          {output?.plaintext && (
            <div className="result-card border-emerald-500/20">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-semibold text-emerald-400 flex items-center gap-2">
                  <UnlockIcon className="w-4 h-4" />
                  Decrypted Successfully
                </span>
                <CopyButton text={output.plaintext} />
              </div>
              <div className="p-3 rounded-lg bg-black/30 text-sm text-gray-300 border border-white/5">
                {output.plaintext}
              </div>
            </div>
          )}
        </div>
      )}

      {/* RSA Mode */}
      {mode === 'rsa' && (
        <div className="space-y-4 fade-in">
          {!output?.private_key ? (
            <button 
              onClick={handleRSAGenerate} 
              disabled={loading}
              className="btn-primary w-full flex items-center justify-center gap-2 py-4"
            >
              <Key className="w-5 h-5" />
              {loading ? 'Generating 2048-bit Key Pair...' : 'Generate RSA Key Pair'}
            </button>
          ) : (
            <div className="space-y-4">
              <div className="result-card border-red-500/20">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-semibold text-red-400 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4" />
                    Private Key (CONFIDENTIAL)
                  </span>
                  <CopyButton text={output.private_key} />
                </div>
                <pre className="p-3 rounded-lg bg-black/30 text-xs font-mono text-gray-400 border border-white/5 overflow-x-auto">
                  {output.private_key}
                </pre>
              </div>
              
              <div className="result-card border-blue-500/20">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-semibold text-blue-400 flex items-center gap-2">
                    <Globe className="w-4 h-4" />
                    Public Key (Shareable)
                  </span>
                  <CopyButton text={output.public_key} />
                </div>
                <pre className="p-3 rounded-lg bg-black/30 text-xs font-mono text-gray-400 border border-white/5 overflow-x-auto">
                  {output.public_key}
                </pre>
              </div>
              
              <div className="pt-4 border-t border-white/10">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Message to encrypt or decrypt..."
                  className="input-field h-24 resize-none mb-3"
                />
                <input
                  type="text"
                  value={key}
                  onChange={(e) => setKey(e.target.value)}
                  placeholder="Paste public key (to encrypt) or private key (to decrypt)"
                  className="input-field mb-3"
                />
                <div className="grid grid-cols-2 gap-3">
                  <button 
                    onClick={handleRSAEncrypt} 
                    disabled={loading || !input || !key}
                    className="btn-primary flex items-center justify-center gap-2"
                  >
                    <Lock className="w-4 h-4" />
                    Encrypt
                  </button>
                  <button 
                    onClick={handleRSADecrypt} 
                    disabled={loading || !input || !key}
                    className="btn-secondary flex items-center justify-center gap-2"
                  >
                    <UnlockIcon className="w-4 h-4" />
                    Decrypt
                  </button>
                </div>
              </div>
              
              {output.ciphertext && (
                <div className="result-card">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-emerald-400">Encrypted Message</span>
                    <CopyButton text={output.ciphertext} />
                  </div>
                  <div className="p-2 rounded bg-black/30 text-xs font-mono break-all text-gray-400">
                    {output.ciphertext}
                  </div>
                </div>
              )}
              
              {output.plaintext && (
                <div className="result-card border-emerald-500/20">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-emerald-400">Decrypted Message</span>
                    <CopyButton text={output.plaintext} />
                  </div>
                  <div className="p-2 rounded bg-black/30 text-sm text-gray-300">
                    {output.plaintext}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          {error}
        </div>
      )}
    </div>
  )
}

// Helper icon component
function UnlockIcon({ className }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
      <path d="M7 11V7a5 5 0 0 1 9.9-1"></path>
    </svg>
  )
}

// PASSWORD TOOLS COMPONENT
function PasswordTools() {
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [result, setResult] = useState(null)
  const [hash, setHash] = useState(null)
  const [loading, setLoading] = useState(false)

  const checkStrength = async () => {
    if (!password) return
    setLoading(true)
    
    try {
      const res = await fetch('/api/password/strength', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      })
      setResult(await res.json())
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const generateHash = async () => {
    if (!password) return
    setLoading(true)
    
    try {
      const res = await fetch('/api/password/hash', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      })
      const data = await res.json()
      setHash(data.hash)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const strengthConfig = [
    { color: '#ff4757', label: 'Very Weak', width: '20%' },
    { color: '#ff6348', label: 'Weak', width: '40%' },
    { color: '#ffa502', label: 'Fair', width: '60%' },
    { color: '#7bed9f', label: 'Strong', width: '80%' },
    { color: '#00ff88', label: 'Very Strong', width: '100%' }
  ]
  
  return (
    <div className="space-y-5 fade-in">
      <div className="relative">
        <input
          type={showPassword ? 'text' : 'password'}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter password to analyze..."
          className="input-field pr-12"
        />
        <button
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 rounded-md hover:bg-white/5 text-gray-500 hover:text-gray-300 transition-colors"
        >
          {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
        </button>
      </div>
      
      <div className="grid grid-cols-2 gap-3">
        <button 
          onClick={checkStrength} 
          disabled={loading || !password}
          className="btn-primary flex items-center justify-center gap-2"
        >
          <Activity className="w-4 h-4" />
          Analyze Strength
        </button>
        <button 
          onClick={generateHash} 
          disabled={loading || !password}
          className="btn-secondary flex items-center justify-center gap-2"
        >
          <Fingerprint className="w-4 h-4" />
          Generate Hash
        </button>
      </div>

      {result && (
        <div className="result-card space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-400">Password Strength</span>
            <span 
              className="text-lg font-bold"
              style={{ color: strengthConfig[result.score].color }}
            >
              {result.strength}
            </span>
          </div>
          
          <div className="strength-bar">
            <div 
              className="strength-fill"
              style={{ 
                width: strengthConfig[result.score].width,
                backgroundColor: strengthConfig[result.score].color
              }}
            />
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Estimated crack time:</span>
            <span className="text-gray-300 font-mono">{result.crack_time}</span>
          </div>
          
          {result.warning && (
            <div className="flex items-start gap-2 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20">
              <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
              <span className="text-sm text-amber-300">{result.warning}</span>
            </div>
          )}
          
          {result.suggestions?.length > 0 && (
            <div className="space-y-2">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Suggestions</span>
              <ul className="space-y-1">
                {result.suggestions.map((s, i) => (
                  <li key={i} className="text-sm text-gray-400 flex items-start gap-2">
                    <ChevronRight className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" />
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {hash && (
        <div className="result-card">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-semibold text-emerald-400 flex items-center gap-2">
              <Fingerprint className="w-4 h-4" />
              bcrypt Hash
            </span>
            <CopyButton text={hash} />
          </div>
          <div className="p-3 rounded-lg bg-black/30 break-all text-xs font-mono text-gray-400 border border-white/5">
            {hash}
          </div>
          <div className="mt-2 text-xs text-gray-500">
            Algorithm: bcrypt • Cost Factor: 12 • Salt: Auto-generated
          </div>
        </div>
      )}
    </div>
  )
}

// PORT SCANNER COMPONENT
function PortScanner() {
  const [target, setTarget] = useState('')
  const [ports, setPorts] = useState('22,80,443,8080')
  const [scanning, setScanning] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState(null)

  const scan = async () => {
    if (!target) return
    setScanning(true)
    setProgress(0)
    setResults(null)
    
    // Simulate progress
    const interval = setInterval(() => {
      setProgress(p => Math.min(p + Math.random() * 15, 90))
    }, 200)
    
    try {
      const res = await fetch('/api/scan/ports', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target, ports })
      })
      const data = await res.json()
      setResults(data)
      setProgress(100)
    } catch (err) {
      console.error(err)
    }
    
    clearInterval(interval)
    setScanning(false)
  }

  return (
    <div className="space-y-5 fade-in">
      <div className="danger-zone">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-sm font-semibold text-red-400 mb-1">Legal Notice</h4>
            <p className="text-xs text-red-300/80 leading-relaxed">
              Only scan systems you own or have explicit written permission to test. 
              Unauthorized port scanning may violate computer fraud and abuse laws.
            </p>
          </div>
        </div>
      </div>
      
      <div className="space-y-3">
        <input
          type="text"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          placeholder="Target IP or hostname (e.g., 127.0.0.1)"
          className="input-field"
        />
        
        <input
          type="text"
          value={ports}
          onChange={(e) => setPorts(e.target.value)}
          placeholder="Port range (e.g., 1-100 or 22,80,443)"
          className="input-field"
        />
        
        <div className="flex gap-2 text-xs">
          <button onClick={() => setPorts('22,80,443')} className="px-2 py-1 rounded bg-white/5 hover:bg-white/10 text-gray-400 transition-colors">Common</button>
          <button onClick={() => setPorts('1-100')} className="px-2 py-1 rounded bg-white/5 hover:bg-white/10 text-gray-400 transition-colors">Quick</button>
          <button onClick={() => setPorts('1-1000')} className="px-2 py-1 rounded bg-white/5 hover:bg-white/10 text-gray-400 transition-colors">Full</button>
        </div>
      </div>
      
      <button 
        onClick={scan} 
        disabled={scanning || !target}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        {scanning ? (
          <>
            <RefreshCw className="w-4 h-4 animate-spin" />
            Scanning {Math.round(progress)}%
          </>
        ) : (
          <>
            <Globe className="w-4 h-4" />
            Start Network Scan
          </>
        )}
      </button>

      {scanning && (
        <div className="h-1 bg-white/10 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-emerald-500 to-cyan-500 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {results && (
        <div className="space-y-3 fade-in">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-400">Target: <span className="text-gray-300 font-mono">{results.target}</span></span>
            <span className="text-emerald-400 font-semibold">{results.open_count} ports open</span>
          </div>
          
          {results.open_ports.length > 0 ? (
            <div className="grid gap-2">
              {results.open_ports.map((port) => (
                <div 
                  key={port.port}
                  className="flex items-center justify-between p-4 rounded-lg bg-emerald-500/5 border border-emerald-500/20 hover:border-emerald-500/40 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="font-mono text-emerald-400 font-semibold">Port {port.port}</span>
                    {port.banner && (
                      <span className="text-xs text-gray-500 truncate max-w-[200px]">{port.banner}</span>
                    )}
                  </div>
                  <span className="badge badge-success text-xs">OPEN</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500 bg-white/5 rounded-lg border border-white/10">
              No open ports detected in specified range
            </div>
          )}
          
          <div className="text-xs text-gray-600 text-center">
            Scanned {results.ports_scanned} ports • {results.open_count} found open
          </div>
        </div>
      )}
    </div>
  )
}

// SECRET SCANNER COMPONENT
function SecretScanner() {
  const [code, setCode] = useState('')
  const [results, setResults] = useState(null)
  const [scanning, setScanning] = useState(false)

  const scan = async () => {
    if (!code) return
    setScanning(true)
    
    try {
      const res = await fetch('/api/scan/secrets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: code })
      })
      setResults(await res.json())
    } catch (err) {
      console.error(err)
    }
    setScanning(false)
  }

  const riskColors = {
    'High': 'text-red-400 bg-red-500/10 border-red-500/20',
    'Medium': 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    'Low': 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
  }

  return (
    <div className="space-y-5 fade-in">
      <div className="relative">
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste code, configuration files, or logs to scan for API keys, passwords, and sensitive tokens..."
          className="input-field h-48 resize-none"
        />
        <div className="absolute bottom-3 right-3 text-xs text-gray-600">
          {code.length} characters
        </div>
      </div>
      
      <button 
        onClick={scan} 
        disabled={scanning || !code}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        {scanning ? (
          <LoadingSpinner />
        ) : (
          <>
            <Search className="w-4 h-4" />
            Scan for Secrets
          </>
        )}
      </button>

      {results && (
        <div className="space-y-3 fade-in">
          <div className={`flex items-center justify-between p-4 rounded-lg border ${riskColors[results.risk_level]}`}>
            <div>
              <span className="text-sm font-semibold">Risk Assessment: {results.risk_level}</span>
              <div className="text-xs opacity-70 mt-0.5">{results.total_found} potential secrets detected</div>
            </div>
            <div className={`text-2xl font-bold ${results.risk_level === 'High' ? 'text-red-400' : results.risk_level === 'Medium' ? 'text-amber-400' : 'text-emerald-400'}`}>
              {results.total_found}
            </div>
          </div>
          
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {results.findings.map((finding, idx) => (
              <div 
                key={idx}
                className="p-3 rounded-lg bg-red-500/5 border border-red-500/10 hover:border-red-500/30 transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-red-400 flex items-center gap-2">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    {finding.type}
                  </span>
                  <span className="text-xs text-gray-500 font-mono">Line {finding.line}</span>
                </div>
                <code className="block p-2 rounded bg-black/30 text-xs font-mono text-gray-400 break-all border border-white/5">
                  {finding.content}
                </code>
              </div>
            ))}
          </div>
          
          {results.total_found === 0 && (
            <div className="text-center py-6 text-emerald-400 bg-emerald-500/5 rounded-lg border border-emerald-500/20">
              <Check className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No secrets detected in provided content</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// WEB TECH DETECTOR COMPONENT
function WebTechDetector() {
  const [url, setUrl] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const detect = async () => {
    if (!url) return
    setLoading(true)
    setResults(null)
    
    try {
      const res = await fetch('/api/detect/webtech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      })
      setResults(await res.json())
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const techColors = {
    'React': 'from-cyan-500/20 to-blue-500/20 text-cyan-400',
    'Vue.js': 'from-emerald-500/20 to-green-500/20 text-emerald-400',
    'Angular': 'from-red-500/20 to-pink-500/20 text-red-400',
    'jQuery': 'from-blue-500/20 to-indigo-500/20 text-blue-400',
    'Bootstrap': 'from-purple-500/20 to-violet-500/20 text-purple-400',
    'WordPress': 'from-blue-500/20 to-cyan-500/20 text-blue-400',
    'Django': 'from-green-500/20 to-emerald-500/20 text-green-400',
    'Flask': 'from-gray-500/20 to-slate-500/20 text-gray-400',
    'Next.js': 'from-gray-500/20 to-white/20 text-gray-300',
    'Laravel': 'from-red-500/20 to-orange-500/20 text-red-400',
    'Ruby on Rails': 'from-red-500/20 to-pink-500/20 text-red-400',
  }

  return (
    <div className="space-y-5 fade-in">
      <div className="relative">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter website URL (e.g., google.com)"
          className="input-field pr-12"
        />
        <Globe className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-600" />
      </div>
      
      <button 
        onClick={detect} 
        disabled={loading || !url}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        {loading ? (
          <LoadingSpinner />
        ) : (
          <>
            <Sparkles className="w-4 h-4" />
            Detect Technologies
          </>
        )}
      </button>

      {results && (
        <div className="result-card space-y-4">
          <div className="flex items-center gap-2 text-sm text-gray-400 pb-3 border-b border-white/5">
            <Globe className="w-4 h-4" />
            <span className="truncate">{results.url}</span>
          </div>
          
          {results.technologies.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {results.technologies.map((tech, idx) => (
                <span 
                  key={idx}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium bg-gradient-to-r ${techColors[tech] || 'from-emerald-500/20 to-cyan-500/20 text-emerald-400'} border border-white/10`}
                >
                  {tech}
                </span>
              ))}
            </div>
          )}
          
          <div className="grid grid-cols-2 gap-3 text-sm">
            {results.server && (
              <div className="p-3 rounded-lg bg-white/5">
                <span className="text-gray-500 block text-xs mb-1">Server</span>
                <span className="text-gray-300 font-mono">{results.server}</span>
              </div>
            )}
            {results.powered_by && (
              <div className="p-3 rounded-lg bg-white/5">
                <span className="text-gray-500 block text-xs mb-1">Powered By</span>
                <span className="text-gray-300">{results.powered_by}</span>
              </div>
            )}
          </div>
          
          {results.technologies.length === 0 && !results.server && (
            <div className="text-center py-6 text-gray-500">
              Unable to detect technologies or site returned no identifying information
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// REPO SCORECARD COMPONENT
function RepoScorecard() {
  const [owner, setOwner] = useState('')
  const [repo, setRepo] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const analyze = async () => {
    if (!owner || !repo) return
    setLoading(true)
    setResults(null)
    
    try {
      const res = await fetch('/api/scorecard', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ owner, repo })
      })
      setResults(await res.json())
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const gradeConfig = {
    'A': { color: '#00ff88', bg: 'from-emerald-500 to-green-400', text: 'Excellent' },
    'B': { color: '#00d4ff', bg: 'from-cyan-500 to-blue-400', text: 'Good' },
    'C': { color: '#ffa502', bg: 'from-amber-500 to-yellow-400', text: 'Fair' },
    'D': { color: '#ff6348', bg: 'from-orange-500 to-red-400', text: 'Poor' },
    'F': { color: '#ff4757', bg: 'from-red-500 to-pink-500', text: 'Critical' }
  }

  const checkIcons = {
    'has_license': <FileCode className="w-4 h-4" />,
    'has_readme': <FileCode className="w-4 h-4" />,
    'has_security_md': <Shield className="w-4 h-4" />,
    'has_codeowners': <Github className="w-4 h-4" />,
    'branch_protection': <Lock className="w-4 h-4" />,
    'requires_pr_reviews': <Eye className="w-4 h-4" />,
    'signed_commits': <Key className="w-4 h-4" />
  }

  const checkLabels = {
    'has_license': 'License File',
    'has_readme': 'README Documentation',
    'has_security_md': 'Security Policy',
    'has_codeowners': 'Code Owners',
    'branch_protection': 'Branch Protection',
    'requires_pr_reviews': 'Required PR Reviews',
    'signed_commits': 'Signed Commits Required'
  }

  return (
    <div className="space-y-5 fade-in">
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <input
            type="text"
            value={owner}
            onChange={(e) => setOwner(e.target.value)}
            placeholder="Owner (e.g., facebook)"
            className="input-field"
          />
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 text-sm">/</span>
        </div>
        <div className="flex-1">
          <input
            type="text"
            value={repo}
            onChange={(e) => setRepo(e.target.value)}
            placeholder="Repository (e.g., react)"
            className="input-field"
          />
        </div>
      </div>
      
      <button 
        onClick={analyze} 
        disabled={loading || !owner || !repo}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        {loading ? (
          <LoadingSpinner />
        ) : (
          <>
            <Activity className="w-4 h-4" />
            Analyze Security Posture
          </>
        )}
      </button>

      {results?.demo_mode && (
        <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/20 text-sm text-amber-200">
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-amber-400">Demo Mode Active</span>
              <p className="mt-1 text-amber-200/80">Set GITHUB_TOKEN environment variable for live repository analysis with real-time data.</p>
            </div>
          </div>
        </div>
      )}

      {results && (
        <div className="result-card space-y-6">
          {/* Header with Grade */}
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-white">{results.repository}</h3>
              <p className="text-sm text-gray-400">Security Scorecard Analysis</p>
            </div>
            <div className="text-center">
              <div 
                className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${gradeConfig[results.grade].bg} flex items-center justify-center text-3xl font-bold text-black shadow-lg`}
              >
                {results.grade}
              </div>
              <span className="text-xs text-gray-500 mt-1 block">{gradeConfig[results.grade].text}</span>
            </div>
          </div>
          
          {/* Score */}
          <div className="text-center py-4 border-y border-white/5">
            <div className="text-4xl font-bold" style={{ color: gradeConfig[results.grade].color }}>
              {results.score}
              <span className="text-xl text-gray-500 font-normal">/{results.max_score}</span>
            </div>
            <div className="text-sm text-gray-500 mt-1">
              {results.percentage || Math.round((results.score/results.max_score)*100)}% compliance
            </div>
          </div>
          
          {/* Checks */}
          {results.checks && (
            <div className="space-y-2">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Security Checks</span>
              <div className="grid gap-2">
                {Object.entries(results.checks).map(([key, passed]) => (
                  <div 
                    key={key}
                    className={`flex items-center justify-between p-3 rounded-lg border ${
                      passed 
                        ? 'bg-emerald-500/5 border-emerald-500/20' 
                        : 'bg-red-500/5 border-red-500/20'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className={passed ? 'text-emerald-400' : 'text-red-400'}>
                        {checkIcons[key] || <Shield className="w-4 h-4" />}
                      </span>
                      <span className="text-sm text-gray-300">{checkLabels[key] || key}</span>
                    </div>
                    <span className={`text-xs font-semibold ${passed ? 'text-emerald-400' : 'text-red-400'}`}>
                      {passed ? 'PASS' : 'FAIL'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// PACKET ANALYZER COMPONENT
function PacketAnalyzer() {
  const [capturing, setCapturing] = useState(false)
  const [interface_, setInterface] = useState('')
  const [duration, setDuration] = useState(30)
  const [packetCount, setPacketCount] = useState(100)
  const [results, setResults] = useState(null)
  const [packets, setPackets] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [statusInterval, setStatusInterval] = useState(null)

  const startCapture = async () => {
    setLoading(true)
    setError(null)
    setPackets([])
    setResults(null)
    
    try {
      const res = await fetch('/api/network/capture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          interface: interface_ || null,
          duration: parseInt(duration),
          packet_count: parseInt(packetCount)
        })
      })
      
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Failed to start capture')
      }
      
      const data = await res.json()
      setCapturing(true)
      
      // Poll for status
      const interval = setInterval(async () => {
        const statusRes = await fetch('/api/network/capture/status')
        const status = await statusRes.json()
        
        setPackets(status.packets || [])
        
        if (!status.capturing && statusInterval) {
          clearInterval(interval)
          setCapturing(false)
          setStatusInterval(null)
          setResults({
            total: status.packets_captured,
            duration: status.elapsed_time
          })
        }
      }, 1000)
      
      setStatusInterval(interval)
      
      // Auto-stop after duration
      setTimeout(() => {
        if (interval) clearInterval(interval)
        setCapturing(false)
        setStatusInterval(null)
      }, duration * 1000)
      
    } catch (err) {
      setError(err.message)
      setCapturing(false)
    }
    setLoading(false)
  }

  const stopCapture = async () => {
    if (statusInterval) {
      clearInterval(statusInterval)
      setStatusInterval(null)
    }
    
    try {
      const res = await fetch('/api/network/capture/stop', { method: 'POST' })
      const data = await res.json()
      setCapturing(false)
      setPackets(data.packets || [])
      setResults({
        total: data.total_packets,
        duration: 'Manual stop'
      })
    } catch (err) {
      console.error(err)
    }
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (statusInterval) clearInterval(statusInterval)
    }
  }, [statusInterval])

  const getProtocolColor = (protocol) => {
    switch(protocol) {
      case 'TCP': return 'text-blue-400 bg-blue-500/10 border-blue-500/20'
      case 'UDP': return 'text-amber-400 bg-amber-500/10 border-amber-500/20'
      default: return 'text-gray-400 bg-gray-500/10 border-gray-500/20'
    }
  }

  const getFlagIcon = (flags) => {
    if (flags === 'S') return <span className="text-red-400 font-bold">SYN</span>
    if (flags === 'SA') return <span className="text-emerald-400">SYN-ACK</span>
    if (flags === 'A') return <span className="text-blue-400">ACK</span>
    if (flags === 'PA') return <span className="text-purple-400">PSH-ACK</span>
    if (flags === 'FA') return <span className="text-gray-400">FIN-ACK</span>
    if (flags === 'R') return <span className="text-red-500">RST</span>
    return <span className="text-gray-500">{flags}</span>
  }

  return (
    <div className="space-y-5 fade-in">
      {/* Admin Warning */}
      <div className="danger-zone">
        <div className="flex items-start gap-3">
          <Shield className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-sm font-semibold text-red-400 mb-1">Administrator Required</h4>
            <p className="text-xs text-red-300/80 leading-relaxed">
              Packet capture requires administrator/root privileges. 
              Run your terminal as Administrator before starting the backend.
              Also ensure Npcap (Windows) or libpcap (Linux/Mac) is installed.
            </p>
          </div>
        </div>
      </div>

      {/* Capture Settings */}
      <div className="grid grid-cols-3 gap-3">
        <div>
          <label className="text-xs text-gray-500 block mb-1">Network Interface</label>
          <input
            type="text"
            value={interface_}
            onChange={(e) => setInterface(e.target.value)}
            placeholder="e.g., eth0, Wi-Fi, or leave blank"
            className="input-field text-sm"
            disabled={capturing}
          />
        </div>
        <div>
          <label className="text-xs text-gray-500 block mb-1">Duration (seconds)</label>
          <input
            type="number"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            min="5"
            max="300"
            className="input-field text-sm"
            disabled={capturing}
          />
        </div>
        <div>
          <label className="text-xs text-gray-500 block mb-1">Max Packets</label>
          <input
            type="number"
            value={packetCount}
            onChange={(e) => setPacketCount(e.target.value)}
            min="10"
            max="1000"
            className="input-field text-sm"
            disabled={capturing}
          />
        </div>
      </div>

      {/* Control Buttons */}
      <div className="flex gap-3">
        {!capturing ? (
          <button 
            onClick={startCapture} 
            disabled={loading}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            {loading ? (
              <LoadingSpinner />
            ) : (
              <>
                <Activity className="w-4 h-4" />
                Start Packet Capture
              </>
            )}
          </button>
        ) : (
          <button 
            onClick={stopCapture}
            className="btn-secondary flex-1 flex items-center justify-center gap-2 bg-red-500/20 border-red-500/30 text-red-400 hover:bg-red-500/30"
          >
            <AlertTriangle className="w-4 h-4" />
            Stop Capture
          </button>
        )}
      </div>

      {/* Status Bar */}
      {capturing && (
        <div className="flex items-center gap-3 p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
          <div className="relative">
            <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse" />
            <div className="absolute inset-0 w-3 h-3 bg-emerald-500 rounded-full animate-ping opacity-75" />
          </div>
          <span className="text-sm text-emerald-400">
            Capturing on {interface_ || 'default interface'}... {packets.length} packets collected
          </span>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Capture Failed</p>
              <p className="mt-1 opacity-80">{error}</p>
              <p className="mt-2 text-xs opacity-60">
                Common fixes: Run as Administrator, install Npcap (Windows), or check interface name
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Results Summary */}
      {results && (
        <div className="result-card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-white">Capture Complete</h3>
            <span className="text-sm text-gray-400">
              {results.total} packets in {typeof results.duration === 'number' ? results.duration.toFixed(1) + 's' : results.duration}
            </span>
          </div>
          
          <div className="grid grid-cols-3 gap-3 mb-4">
            <div className="p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 text-center">
              <div className="text-2xl font-bold text-blue-400">
                {packets.filter(p => p.protocol === 'TCP').length}
              </div>
              <div className="text-xs text-gray-500">TCP Packets</div>
            </div>
            <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-center">
              <div className="text-2xl font-bold text-amber-400">
                {packets.filter(p => p.protocol === 'UDP').length}
              </div>
              <div className="text-xs text-gray-500">UDP Packets</div>
            </div>
            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-center">
              <div className="text-2xl font-bold text-red-400">
                {packets.filter(p => p.alert).length}
              </div>
              <div className="text-xs text-gray-500">Alerts</div>
            </div>
          </div>
        </div>
      )}

      {/* Packet List */}
      {packets.length > 0 && (
        <div className="space-y-2 max-h-96 overflow-y-auto">
          <div className="flex items-center justify-between text-xs text-gray-500 sticky top-0 bg-[#12121a] py-2">
            <span>Captured Packets</span>
            <span>{packets.length} total</span>
          </div>
          
          {packets.map((packet, idx) => (
            <div 
              key={idx}
              className={`p-3 rounded-lg border text-sm space-y-2 ${
                packet.alert 
                  ? 'bg-red-500/5 border-red-500/30' 
                  : 'bg-white/5 border-white/10 hover:border-white/20'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getProtocolColor(packet.protocol)}`}>
                    {packet.protocol}
                  </span>
                  {packet.flags && getFlagIcon(packet.flags)}
                  {packet.alert && (
                    <span className="badge badge-danger text-xs">
                      <AlertTriangle className="w-3 h-3 inline mr-1" />
                      ALERT
                    </span>
                  )}
                </div>
                <span className="text-xs text-gray-500 font-mono">
                  {new Date(packet.timestamp * 1000).toLocaleTimeString()}
                </span>
              </div>
              
              <div className="flex items-center gap-2 text-xs font-mono text-gray-400">
                <span className="text-emerald-400">{packet.src_ip}</span>
                {packet.src_port && <span>:{packet.src_port}</span>}
                <span className="text-gray-600">→</span>
                <span className="text-blue-400">{packet.dst_ip}</span>
                {packet.dst_port && <span>:{packet.dst_port}</span>}
              </div>
              
              {packet.http_request && (
                <div className="p-2 rounded bg-purple-500/10 border border-purple-500/20">
                  <span className="text-xs text-purple-400 font-medium">HTTP Request</span>
                  <div className="text-xs text-gray-300 mt-1 font-mono">{packet.http_request}</div>
                </div>
              )}
              
              {packet.payload_preview && (
                <div className="text-xs text-gray-500 font-mono truncate">
                  Payload: {packet.payload_preview}
                </div>
              )}
              
              {packet.alert && (
                <div className="text-xs text-red-400 font-medium">
                  {packet.alert}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// MAIN APP COMPONENT
export default function App() {
  const [activeTool, setActiveTool] = useState(null)

  const renderTool = () => {
    switch (activeTool) {
      case 'crypto': return <CryptoToolkit />
      case 'password': return <PasswordTools />
      case 'portscan': return <PortScanner />
      case 'secrets': return <SecretScanner />
      case 'webtech': return <WebTechDetector />
      case 'scorecard': return <RepoScorecard />
      case 'packets': return <PacketAnalyzer />
      default: return null
    }
  }

  const activeToolData = tools.find(t => t.id === activeTool)

  return (
    <div className="min-h-screen grid-bg">
      {/* Header */}
      <header className="header-glow sticky top-0 z-50 backdrop-blur-xl">
        <div className="container mx-auto max-w-6xl px-6 py-4">
          <div 
            className="flex items-center gap-4 cursor-pointer group"
            onClick={() => setActiveTool(null)}
          >
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:shadow-emerald-500/40 transition-shadow">
                <Terminal className="w-5 h-5 text-black" />
              </div>
              <div className="absolute inset-0 rounded-xl bg-emerald-500/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white tracking-tight">Security Toolkit</h1>
              <p className="text-xs text-gray-500 font-medium tracking-wide uppercase">Unified Cybersecurity Platform</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto max-w-6xl px-6 py-12">
        {activeTool ? (
          <div className="max-w-2xl mx-auto slide-in">
            <button 
              onClick={() => setActiveTool(null)}
              className="flex items-center gap-2 text-gray-500 hover:text-white mb-6 transition-colors group"
            >
              <div className="p-2 rounded-lg bg-white/5 group-hover:bg-white/10 transition-colors">
                <ArrowLeft className="w-4 h-4" />
              </div>
              <span className="text-sm font-medium">Back to Dashboard</span>
            </button>
            
            <div className="bg-[#12121a] border border-[#2a2a3a] rounded-2xl p-8 shadow-2xl">
              <div className="flex items-center gap-4 mb-8 pb-6 border-b border-white/5">
                {activeToolData && (
                  <>
                    <div 
                      className="w-14 h-14 rounded-xl flex items-center justify-center"
                      style={{ 
                        background: `linear-gradient(135deg, ${activeToolData.color}20, ${activeToolData.color}05)`,
                        border: `1px solid ${activeToolData.color}30`
                      }}
                    >
                      <activeToolData.icon className="w-7 h-7" style={{ color: activeToolData.color }} />
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-white">{activeToolData.name}</h2>
                      <p className="text-sm text-gray-400 mt-0.5">{activeToolData.description}</p>
                    </div>
                  </>
                )}
              </div>
              
              {renderTool()}
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            <div className="text-center max-w-2xl mx-auto mb-12">
              <h2 className="text-3xl font-bold mb-3 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                Security Tools Dashboard
              </h2>
              <p className="text-gray-500">
                Professional cybersecurity utilities for analysis, testing, and hardening
              </p>
            </div>
            
            <div className="card-grid">
              {tools.map((tool) => {
                const Icon = tool.icon
                return (
                  <div
                    key={tool.id}
                    onClick={() => setActiveTool(tool.id)}
                    className="card group"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div 
                        className="tool-icon-wrapper"
                        style={{ borderColor: `${tool.color}30` }}
                      >
                        <Icon className="w-6 h-6" style={{ color: tool.color }} />
                      </div>
                      <ChevronRight className="w-5 h-5 text-gray-600 group-hover:text-white transition-colors" />
                    </div>
                    
                    <h3 className="text-lg font-bold text-white mb-2 group-hover:text-emerald-400 transition-colors">
                      {tool.shortName}
                    </h3>
                    <p className="text-sm text-gray-500 leading-relaxed">
                      {tool.description}
                    </p>
                    
                    <div className="mt-4 pt-4 border-t border-white/5 flex items-center gap-2 text-xs text-gray-600">
                      <Zap className="w-3 h-3" style={{ color: tool.color }} />
                      <span style={{ color: tool.color }}>Click to launch</span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}
      </main>
      
      {/* Footer */}
      <footer className="border-t border-white/5 mt-20 py-8">
        <div className="container mx-auto max-w-6xl px-6 text-center text-sm text-gray-600">
          <p>Security Toolkit • Professional Cybersecurity Utilities</p>
          <p className="mt-1 text-xs">For authorized security testing and educational purposes only</p>
        </div>
      </footer>
    </div>
  )
}