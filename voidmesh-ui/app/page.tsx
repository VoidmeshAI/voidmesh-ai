"use client"

import { useEffect, useState } from "react"

async function getLeaderboard() {

  const res = await fetch(
    "https://voidmesh-ai.onrender.com/leaderboard",
    {
      cache: "no-store"
    }
  )

  return res.json()
}

export default function Home() {

  const [portfolio, setPortfolio] = useState({

    balance: 0,
    pnl: 0,
    growth: 0
  })

  const [leaderboard, setLeaderboard] = useState<any[]>([])

  useEffect(() => {

    // ==========================================
    // WEBSOCKET
    // ==========================================

    const socket = new WebSocket(
      "wss://voidmesh-ai.onrender.com/ws"
    )

    socket.onmessage = (event) => {

      const data = JSON.parse(event.data)

      setPortfolio(data)
    }

    // ==========================================
    // LOAD LEADERBOARD
    // ==========================================

    async function loadLeaderboard() {

      try {

        const data = await getLeaderboard()

        setLeaderboard(
          data.leaderboard
        )

      } catch (error) {

        console.log(
          "Leaderboard Error",
          error
        )
      }
    }

    loadLeaderboard()

    return () => {

      socket.close()
    }

  }, [])

  return (

    <main className="min-h-screen bg-black text-white p-6">

      {/* HEADER */}

      <h1 className="text-5xl font-bold text-cyan-400 mb-8">

        VOIDMESH AI

      </h1>

      {/* GRID */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* PORTFOLIO */}

        <div className="bg-zinc-900 p-6 rounded-2xl shadow-lg">

          <h2 className="text-2xl mb-4 text-cyan-400">

            💰 Live Portfolio

          </h2>

          <div className="space-y-3">

            <p className="text-lg">

              Balance:
              <span className="text-green-400 ml-2">
                ${portfolio.balance}
              </span>

            </p>

            <p className="text-lg">

              PNL:
              <span className="text-yellow-400 ml-2">
                ${portfolio.pnl}
              </span>

            </p>

            <p className="text-lg">

              Growth:
              <span className="text-cyan-400 ml-2">
                {portfolio.growth}%
              </span>

            </p>

          </div>

        </div>

        {/* LEADERBOARD */}

        <div className="bg-zinc-900 p-6 rounded-2xl shadow-lg">

          <h2 className="text-2xl mb-4 text-cyan-400">

            🏆 Leaderboard

          </h2>

          <div className="space-y-4">

            {
              leaderboard.map(
                (user: any, index: number) => (

                  <div
                    key={index}
                    className="
                      border
                      border-zinc-800
                      rounded-xl
                      p-4
                      bg-zinc-950
                    "
                  >

                    <p className="text-lg font-bold">

                      #{index + 1}
                      {" "}
                      {user[0]}

                    </p>

                    <p>

                      💰 Balance:
                      {" "}
                      ${user[1]}

                    </p>

                    <p>

                      📈 PNL:
                      {" "}
                      ${user[2]}

                    </p>

                    <p>

                      🎯 Winrate:
                      {" "}
                      {user[3]}%

                    </p>

                  </div>
                )
              )
            }

          </div>

        </div>

      </div>

    </main>
  )
}