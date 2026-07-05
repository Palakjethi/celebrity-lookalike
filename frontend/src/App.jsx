import { useState } from "react"
import Landing from "./pages/Landing"
import Results from "./pages/Results"

export default function App() {
  const [page, setPage] = useState("landing")
  const [results, setResults] = useState(null)
  const [userPhoto, setUserPhoto] = useState(null)
  const [filters, setFilters] = useState({ gender: "any", industry: "both" })

  return (
    <>
      {page === "landing" && (
        <Landing
          filters={filters}
          setFilters={setFilters}
          onResults={(data, photo) => {
            setResults(data)
            setUserPhoto(photo)
            setPage("results")
          }}
        />
      )}
      {page === "results" && (
        <Results
          results={results}
          userPhoto={userPhoto}
          onBack={() => setPage("landing")}
        />
      )}
    </>
  )
}