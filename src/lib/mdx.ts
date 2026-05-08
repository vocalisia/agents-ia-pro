import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'

const BLOG_DIR = path.join(process.cwd(), 'content/blog')

export interface BlogPost {
  slug: string
  title: string
  description: string
  date: string
  author: string
  category: string
  readTime: string
  image?: string
  content: string
}

export interface BlogPostMeta extends Omit<BlogPost, 'content'> {}

function ensureBlogDir(): void {
  if (!fs.existsSync(BLOG_DIR)) {
    fs.mkdirSync(BLOG_DIR, { recursive: true })
  }
}

export function getAllPostSlugs(): string[] {
  ensureBlogDir()
  return fs
    .readdirSync(BLOG_DIR)
    .filter((file) => file.endsWith('.mdx') || file.endsWith('.md'))
    .map((file) => file.replace(/\.(mdx|md)$/, ''))
}

export function getAllPosts(): BlogPostMeta[] {
  const slugs = getAllPostSlugs()
  return slugs
    .map((slug) => getPostMeta(slug))
    .filter((p): p is BlogPostMeta => p !== null)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
}

export function getPostMeta(slug: string): BlogPostMeta | null {
  const filePath = resolvePostPath(slug)
  if (!filePath) return null

  const raw = fs.readFileSync(filePath, 'utf-8')
  const { data } = matter(raw)

  return {
    slug,
    title: data.title ?? slug,
    description: data.description ?? '',
    date: data.date ? String(data.date) : '',
    author: data.author ?? 'Laurent Duplat',
    category: data.category ?? 'Guide',
    readTime: data.readTime ?? '5 min de lecture',
    image: data.image,
  }
}

export function getPost(slug: string): BlogPost | null {
  const filePath = resolvePostPath(slug)
  if (!filePath) return null

  const raw = fs.readFileSync(filePath, 'utf-8')
  const { data, content } = matter(raw)

  return {
    slug,
    title: data.title ?? slug,
    description: data.description ?? '',
    date: data.date ? String(data.date) : '',
    author: data.author ?? 'Laurent Duplat',
    category: data.category ?? 'Guide',
    readTime: data.readTime ?? '5 min de lecture',
    image: data.image,
    content,
  }
}

function resolvePostPath(slug: string): string | null {
  ensureBlogDir()
  const mdx = path.join(BLOG_DIR, `${slug}.mdx`)
  const md = path.join(BLOG_DIR, `${slug}.md`)
  if (fs.existsSync(mdx)) return mdx
  if (fs.existsSync(md)) return md
  return null
}

export function formatDate(dateStr: string): string {
  if (!dateStr) return ''
  try {
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    })
  } catch {
    return dateStr
  }
}
