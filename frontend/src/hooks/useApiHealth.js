import { useEffect, useState } from 'react'
import { getHealth } from '@/api/client'

export function useApiHealth(intervalMs = 30000) {
  const [status, setStatus] = useState({ online: false, modelLoaded: false, modelName: null, checking: true })

  useEffect(() => {
    let cancelled = false

    async function check() {
      try {
        const data = await getHealth()
        if (cancelled) return
        setStatus({
          online: data?.status === 'ok' || data?.status === 'healthy' || !!data,
          modelLoaded: !!data?.model_loaded,
          modelName: data?.model_name || null,
          checking: false,
        })
      } catch {
        if (cancelled) return
        setStatus({ online: false, modelLoaded: false, modelName: null, checking: false })
      }
    }

    check()
    const id = setInterval(check, intervalMs)
    return () => {
      cancelled = true
      clearInterval(id)
    }
  }, [intervalMs])

  return status
}
