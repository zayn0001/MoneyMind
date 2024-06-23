import { Terminal } from "lucide-react"

import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"

export default function Info({ company, sentiment }) {
  return (
    <div className="p-5 w-full">
    <Alert style={{width:"100%"}}>
      <Terminal className="h-4 w-4" />
      <AlertTitle>{company}</AlertTitle>
      <AlertDescription>
        {sentiment}
      </AlertDescription>
    </Alert>
    </div>
  )
}
