import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

export function formatEUR(value) {
  if (value == null || isNaN(value)) return '— €'
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(value)
}

export function formatNumber(value) {
  if (value == null || isNaN(value)) return '—'
  return new Intl.NumberFormat('fr-FR').format(value)
}

export function formatPct(value, digits = 1) {
  if (value == null || isNaN(value)) return '—'
  return `${(value * 100).toFixed(digits)}%`
}
