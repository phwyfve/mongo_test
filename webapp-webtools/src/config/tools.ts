export interface Tool {
  id: string
  name: string
  description: string
  acceptedFormats: string[]
  icon: string
  color: string
}

export interface Category {
  id: string
  name: string
  description: string
  color: string
  borderColor: string
  bgColor: string
  tools: Tool[]
}

export const categories: Category[] = [
  {
    id: 'merge',
    name: 'Merge',
    description: 'Combine multiple files into one',
    color: 'text-blue-700',
    borderColor: 'border-blue-500',
    bgColor: 'bg-blue-50 hover:bg-blue-100',
    tools: [
      {
        id: 'merge-pdf',
        name: 'Merge PDFs',
        description: 'Combine multiple PDF files into a single document',
        acceptedFormats: ['.pdf'],
        icon: '📄',
        color: 'text-blue-600',
      },
      {
        id: 'merge-images',
        name: 'Merge Images',
        description: 'Combine multiple images into one collage',
        acceptedFormats: ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        icon: '🖼️',
        color: 'text-blue-600',
      },
    ],
  },
  {
    id: 'convert',
    name: 'Convert to PDF',
    description: 'Convert various file formats to PDF',
    color: 'text-green-700',
    borderColor: 'border-green-500',
    bgColor: 'bg-green-50 hover:bg-green-100',
    tools: [
      {
        id: 'docx-to-pdf',
        name: 'Word to PDF',
        description: 'Convert Microsoft Word documents to PDF',
        acceptedFormats: ['.docx', '.doc'],
        icon: '📝',
        color: 'text-green-600',
      },
      {
        id: 'excel-to-pdf',
        name: 'Excel to PDF',
        description: 'Convert Excel spreadsheets to PDF',
        acceptedFormats: ['.xlsx', '.xls'],
        icon: '📊',
        color: 'text-green-600',
      },
      {
        id: 'ppt-to-pdf',
        name: 'PowerPoint to PDF',
        description: 'Convert PowerPoint presentations to PDF',
        acceptedFormats: ['.pptx', '.ppt'],
        icon: '📈',
        color: 'text-green-600',
      },
      {
        id: 'image-to-pdf',
        name: 'Images to PDF',
        description: 'Convert images to PDF format',
        acceptedFormats: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
        icon: '🖼️',
        color: 'text-green-600',
      },
    ],
  },
]

export const getCategoryById = (id: string): Category | undefined => {
  return categories.find(category => category.id === id)
}

export const getToolById = (categoryId: string, toolId: string): Tool | undefined => {
  const category = getCategoryById(categoryId)
  return category?.tools.find(tool => tool.id === toolId)
}
