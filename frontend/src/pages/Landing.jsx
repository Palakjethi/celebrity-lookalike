import { useRef, useState, useEffect } from "react"
import axios from "axios"
import styles from "./Landing.module.css"

export default function Landing({ filters, setFilters, onResults }) {
  const [dragging, setDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [landingCelebs, setLandingCelebs] = useState([])
  const fileRef = useRef()

  useEffect(() => {
    axios.get("https://celebrity-lookalike-api.onrender.com/landing-celebs")
      .then(res => setLandingCelebs(res.data.celebs))
      .catch(() => {})
  }, [])

  const col1 = landingCelebs.slice(0, 6)
  const col2 = landingCelebs.slice(6, 12)

  async function handleFile(file) {
    if (!file) return
    setError(null)
    setLoading(true)
    const photoURL = URL.createObjectURL(file)
    const formData = new FormData()
    formData.append("file", file)
    formData.append("gender", filters.gender)
    formData.append("industry", filters.industry)
    try {
      const res = await axios.post("https://celebrity-lookalike-api.onrender.com/match", formData)
      if (res.data.error) {
        setError(res.data.error)
      } else {
        onResults(res.data.matches, photoURL)
      }
    } catch (e) {
      setError("Could not connect to the server. Make sure the API is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.left}>
        <div className={styles.eyebrow}>AI face matching · 930+ celebrities</div>
        <h1 className={styles.headline}>
          Your face.<br /><em>Their</em> fame.
        </h1>
        <p className={styles.tagline}>"Every face has a star — find yours."</p>
        <p className={styles.sub}>
          Upload a photo and our AI finds your closest celebrity match
          across Bollywood and Hollywood in seconds. Zero photos stored.
        </p>

        <div className={styles.filterLabel}>Match me with</div>
        <div className={styles.pills}>
          {["any", "male", "female"].map(g => (
            <button
              key={g}
              className={filters.gender === g ? styles.pillActive : styles.pill}
              onClick={() => setFilters(f => ({ ...f, gender: g }))}
            >
              {g === "any" ? "Any gender" : g.charAt(0).toUpperCase() + g.slice(1)}
            </button>
          ))}
        </div>

        <div className={styles.pills} style={{ marginTop: 8 }}>
          {[
            { val: "both", label: "Bollywood + Hollywood" },
            { val: "bollywood", label: "Bollywood only" },
            { val: "hollywood", label: "Hollywood only" },
          ].map(i => (
            <button
              key={i.val}
              className={filters.industry === i.val ? styles.pillActive : styles.pill}
              onClick={() => setFilters(f => ({ ...f, industry: i.val }))}
            >
              {i.label}
            </button>
          ))}
        </div>

        <div
          className={`${styles.dropzone} ${dragging ? styles.dropzoneActive : ""}`}
          onDragOver={e => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={e => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files[0]) }}
          onClick={() => fileRef.current.click()}
        >
          {loading ? (
            <div className={styles.loadingText}>Finding your celebrity twin...</div>
          ) : (
            <>
              <div className={styles.uploadIcon}>↑</div>
              <div className={styles.uploadText}>Drop your photo here</div>
              <div className={styles.uploadSub}>or click to browse</div>
            </>
          )}
        </div>

        <input
          ref={fileRef}
          type="file"
          accept="image/*"
          style={{ display: "none" }}
          onChange={e => handleFile(e.target.files[0])}
        />

        {error && <div className={styles.error}>{error}</div>}

        <div className={styles.stats}>
          <div><div className={styles.statNum}>930+</div><div className={styles.statLabel}>Celebrities</div></div>
          <div><div className={styles.statNum}>ArcFace</div><div className={styles.statLabel}>AI model</div></div>
          <div><div className={styles.statNum}>0 stored</div><div className={styles.statLabel}>Your photos</div></div>
        </div>
      </div>

      <div className={styles.right}>
        <div className={styles.fadeTop} />
        <div className={styles.fadeBottom} />
        <div className={styles.cols}>
          <div className={styles.col}>
            <div className={styles.scrollTrack}>
              {[...col1, ...col1, ...col1, ...col1].map((c, i) => (
                <CelebCard key={`c1-${i}`} celeb={c} />
              ))}
            </div>
          </div>
          <div className={styles.col}>
            <div className={styles.scrollTrack2}>
              {[...col2, ...col2, ...col2, ...col2].map((c, i) => (
                <CelebCard key={`c2-${i}`} celeb={c} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function CelebCard({ celeb }) {
  const [imgError, setImgError] = useState(false)

  return (
    <div style={{
      borderRadius: 10,
      overflow: "hidden",
      border: "1.5px solid #2A1005",
      flexShrink: 0,
      width: "100%",
    }}>
      <div style={{
        height: 160,
        background: "#2A1005",
        overflow: "hidden",
      }}>
        {celeb.photo_url && !imgError ? (
          <img
            src={celeb.photo_url}
            alt={celeb.name}
            onError={() => setImgError(true)}
            style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "center" }}
          />
        ) : (
          <div style={{ width: "100%", height: "100%", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <svg width="38" height="38" viewBox="0 0 40 40">
              <circle cx="20" cy="14" r="9" fill="#C47050" opacity=".6" />
              <ellipse cx="20" cy="33" rx="13" ry="8" fill="#C47050" opacity=".5" />
            </svg>
          </div>
        )}
      </div>
    </div>
  )
}