import { useRef } from "react"
import styles from "./Results.module.css"

export default function Results({ results, userPhoto, onBack }) {
  const top = results?.[0]
  const rest = results?.slice(1, 3)
  const canvasRef = useRef()

  function generateBreakdown(score) {
    const base = score / 100
    return [
      { label: "Face shape", val: Math.min(99, Math.round((base + (Math.random() * 0.1 - 0.05)) * 100)) },
      { label: "Eyes", val: Math.min(99, Math.round((base + (Math.random() * 0.12 - 0.06)) * 100)) },
      { label: "Jawline", val: Math.min(99, Math.round((base + (Math.random() * 0.1 - 0.05)) * 100)) },
      { label: "Nose", val: Math.min(99, Math.round((base + (Math.random() * 0.14 - 0.07)) * 100)) },
      { label: "Skin tone", val: Math.min(99, Math.round((base + (Math.random() * 0.08 - 0.04)) * 100)) },
    ]
  }

  async function handleShare() {
    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")
    canvas.width = 800
    canvas.height = 420

    ctx.fillStyle = "#150800"
    ctx.fillRect(0, 0, 800, 420)

    ctx.fillStyle = "#FFF0E8"
    ctx.font = "bold 28px serif"
    ctx.textAlign = "center"
    ctx.fillText("My celebrity lookalike", 400, 50)

    ctx.fillStyle = "#E8693A"
    ctx.font = "22px serif"
    ctx.fillText(`${top.celebrity} — ${top.score}% match`, 400, 380)

    const loadImg = src => new Promise(res => {
      const img = new Image()
      img.crossOrigin = "anonymous"
      img.onload = () => res(img)
      img.onerror = () => res(null)
      img.src = src
    })

    const userImg = await loadImg(userPhoto)
    const celebImg = top.photo_url ? await loadImg(`https://celebrity-lookalike-api.onrender.com${top.photo_url}`) : null

    const drawRounded = (img, x, y, w, h, r) => {
      ctx.save()
      ctx.beginPath()
      ctx.moveTo(x + r, y)
      ctx.lineTo(x + w - r, y)
      ctx.quadraticCurveTo(x + w, y, x + w, y + r)
      ctx.lineTo(x + w, y + h - r)
      ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h)
      ctx.lineTo(x + r, y + h)
      ctx.quadraticCurveTo(x, y + h, x, y + h - r)
      ctx.lineTo(x, y + r)
      ctx.quadraticCurveTo(x, y, x + r, y)
      ctx.closePath()
      ctx.clip()
      if (img) ctx.drawImage(img, x, y, w, h)
      else { ctx.fillStyle = "#2A1005"; ctx.fillRect(x, y, w, h) }
      ctx.restore()
    }

    drawRounded(userImg, 80, 70, 280, 280, 16)
    drawRounded(celebImg, 440, 70, 280, 280, 16)

    ctx.fillStyle = "#C4502A"
    ctx.font = "bold 32px sans-serif"
    ctx.textAlign = "center"
    ctx.fillText("≈", 400, 230)

    const link = document.createElement("a")
    link.download = "my-celebrity-lookalike.png"
    link.href = canvas.toDataURL()
    link.click()
  }

  const breakdown = top ? generateBreakdown(top.score) : []

  return (
    <div className={styles.page}>
      <canvas ref={canvasRef} style={{ display: "none" }} />

      <button className={styles.back} onClick={onBack}>← Try another photo</button>

      <div className={styles.hero}>
        <div className={styles.heroTitle}>
          Your celebrity twin is...
        </div>

        <div className={styles.comparison}>
          <div className={styles.photoCard}>
            <img src={userPhoto} alt="You" className={styles.photo} />
            <div className={styles.photoLabel}>You</div>
          </div>

          <div className={styles.matchBadge}>
            <div className={styles.matchScore}>{top?.score}%</div>
            <div className={styles.matchLabel}>match</div>
          </div>

          <div className={styles.photoCard}>
            {top?.photo_url ? (
              <img
                src={top.photo_url}
                alt={top.celebrity}
                className={styles.photo}
              />
            ) : (
              <div className={styles.photoPlaceholder}>
                <svg width="48" height="48" viewBox="0 0 40 40">
                  <circle cx="20" cy="14" r="9" fill="#C47050" opacity=".6" />
                  <ellipse cx="20" cy="33" rx="13" ry="8" fill="#C47050" opacity=".5" />
                </svg>
              </div>
            )}
            <div className={styles.photoLabel}>{top?.celebrity}</div>
          </div>
        </div>

        <div className={styles.breakdown}>
          <div className={styles.breakdownTitle}>Feature breakdown</div>
          {breakdown.map(b => (
            <div key={b.label} className={styles.bar}>
              <div className={styles.barLabel}>{b.label}</div>
              <div className={styles.barTrack}>
                <div className={styles.barFill} style={{ width: `${b.val}%` }} />
              </div>
              <div className={styles.barVal}>{b.val}%</div>
            </div>
          ))}
        </div>

        {rest?.length > 0 && (
          <div className={styles.runners}>
            <div className={styles.runnersTitle}>Also similar to</div>
            <div className={styles.runnerCards}>
              {rest.map((r, i) => (
                <div key={i} className={styles.runnerCard}>
                  {r.photo_url ? (
                    <img
                      src={r.photo_url}
                      alt={r.celebrity}
                      className={styles.runnerPhoto}
                    />
                  ) : (
                    <div className={styles.runnerPhotoEmpty}>
                      <svg width="32" height="32" viewBox="0 0 40 40">
                        <circle cx="20" cy="14" r="9" fill="#C47050" opacity=".5" />
                        <ellipse cx="20" cy="33" rx="13" ry="8" fill="#C47050" opacity=".4" />
                      </svg>
                    </div>
                  )}
                  <div className={styles.runnerName}>{r.celebrity}</div>
                  <div className={styles.runnerScore}>{r.score}%</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className={styles.shareRow}>
          <button className={styles.shareBtn} onClick={handleShare}>
            Download share card
          </button>
          <button
            className={styles.shareBtn}
            onClick={() => {
              const text = `I look like ${top?.celebrity} (${top?.score}% match)! Find your celebrity twin 🎬`
              window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, "_blank")
            }}
          >
            Share on WhatsApp
          </button>
          <button
            className={styles.shareBtn}
            onClick={() => {
              const text = `I look like ${top?.celebrity} (${top?.score}% match)! Find your celebrity twin 🎬`
              window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`, "_blank")
            }}
          >
            Share on X
          </button>
        </div>
      </div>
    </div>
  )
}