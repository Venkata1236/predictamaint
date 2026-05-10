import {
    useEffect,
    useRef,
    useState,
} from "react"

const useWebSocket = (url) => {
    const [data, setData] =
        useState(null)

    const [status, setStatus] =
        useState("connecting")

    const wsRef = useRef(null)

    useEffect(() => {

        const connect = () => {

            wsRef.current =
                new WebSocket(url)

            wsRef.current.onopen = () => {
                setStatus("connected")
            }

            wsRef.current.onmessage = (
                event
            ) => {

                const parsedData =
                    JSON.parse(event.data)

                setData(parsedData)
            }

            wsRef.current.onclose = () => {

                setStatus(
                    "reconnecting"
                )

                setTimeout(
                    connect,
                    3000
                )
            }
        }

        connect()

        return () => {
            wsRef.current?.close()
        }

    }, [url])

    return {
        data,
        status,
    }
}

export default useWebSocket