import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { useToast } from '../contexts/ToastContext'
import { processApi } from '../services/api'

export default function SplitPdf() {
  const navigate = useNavigate()
  const { token } = useAuth()
  const { addToast } = useToast()

  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [dragOver, setDragOver] = useState(false)
  const [processing, setProcessing] = useState(false)

  const handleFileSelect = useCallback((files: FileList | null) => {
    if (!files || files.length === 0) return

    const file = files[0]
    const extension = '.' + file.name.split('.').pop()?.toLowerCase()
    
    if (extension !== '.pdf') {
      addToast({
        title: 'Invalid file format',
        description: 'Only PDF files are supported',
        variant: 'destructive',
      })
      return
    }

    setSelectedFile(file)
  }, [addToast])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setDragOver(false)
      handleFileSelect(e.dataTransfer.files)
    },
    [handleFileSelect]
  )

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
  }, [])

  const removeFile = () => {
    setSelectedFile(null)
  }

  const handleProcess = async () => {
    if (!selectedFile) return

    setProcessing(true)
    try {
      const response = await processApi.createSplitPdfCommand(selectedFile)
      const commandId = response.command_id

      // Navigate to wait page with command_id
      navigate(`/wait/${commandId}`)
      
    } catch (error) {
      addToast({
        title: 'Processing failed',
        description: error instanceof Error ? error.message : 'Network error occurred',
        variant: 'destructive',
      })
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <nav className="text-sm text-gray-500 mb-4">
          <button onClick={() => navigate('/')} className="hover:text-blue-600">
            Home
          </button>
          <span className="mx-2">/</span>
          <span className="text-blue-600">Split</span>
          <span className="mx-2">/</span>
          <span className="text-gray-900">Split PDF</span>
        </nav>

        <div className="flex items-start space-x-4">
          <div className="text-4xl">✂️</div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Split PDF</h1>
            <p className="text-gray-600 text-lg">
              Split a PDF file into individual pages packaged as a ZIP archive
            </p>
          </div>
        </div>
      </div>

      {/* File Upload Area */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload PDF File</h2>
        
        {/* Accepted Formats */}
        <div className="mb-6">
          <p className="text-sm text-gray-600 mb-2">Accepted format:</p>
          <span className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full font-mono">
            .pdf
          </span>
        </div>

        {/* Drop Zone */}
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragOver
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          <div className="space-y-4">
            <div className="text-4xl text-gray-400">📄</div>
            <div>
              <p className="text-lg font-medium text-gray-900">
                Drop PDF file here or click to select
              </p>
              <p className="text-gray-500">
                Upload one PDF file to split into pages
              </p>
            </div>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => handleFileSelect(e.target.files)}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer transition-colors"
            >
              Select PDF File
            </label>
          </div>
        </div>

        {/* Selected File */}
        {selectedFile && (
          <div className="mt-6 space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Selected File</h3>
            <div className="border border-gray-200 rounded-lg p-4 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">📄</span>
                <div>
                  <p className="font-medium text-gray-900">{selectedFile.name}</p>
                  <p className="text-sm text-gray-500">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <button
                onClick={removeFile}
                className="text-red-600 hover:text-red-700 p-2"
                title="Remove file"
              >
                ✕
              </button>
            </div>
          </div>
        )}

        {/* Process Button */}
        {selectedFile && (
          <div className="mt-6 flex justify-end">
            <button
              onClick={handleProcess}
              disabled={processing}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {processing ? (
                <>
                  <span className="inline-block animate-spin mr-2">⚙️</span>
                  Processing...
                </>
              ) : (
                <>
                  ✂️ Split PDF
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Info Card */}
      <div className="mt-8 card bg-blue-50 border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-900 mb-2">ℹ️ How it works</h3>
        <ul className="space-y-2 text-blue-800">
          <li className="flex items-start">
            <span className="mr-2">1️⃣</span>
            <span>Upload your PDF file</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">2️⃣</span>
            <span>Each page will be extracted as a separate PDF</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">3️⃣</span>
            <span>All pages are packaged into a ZIP archive</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">4️⃣</span>
            <span>Download the ZIP file with all individual pages</span>
          </li>
        </ul>
      </div>
    </div>
  )
}
