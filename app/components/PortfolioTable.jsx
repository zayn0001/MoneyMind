import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

export default function PortfolioTable({ invoices, fetchportfolio, user }) {

  const handleremovecompany = async (companyname)=>{
    try {
      const response = await fetch("/backend/removecompany", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${user.accessToken}`,
          'Content-Type': 'application/json'
        },
        body:JSON.stringify({company:companyname})
      });
  
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      
      const responseData = await response.json();
      console.log(responseData)
      fetchportfolio(user.accessToken)
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
  return (
    <div className="w-auto">
    <Table>
      <TableCaption>A list of your companies that you have invested in</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead className="text-xl w-[300px] text-center">Companies</TableHead>
          <TableHead className="text-xl w-[50px] text-center"></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {invoices.map((invoice) => (
          <TableRow key={invoice.invoice}>
            <TableCell className="font-medium text-center">{invoice.name}</TableCell>
            <TableCell className="font-medium text-center"><Button 
        variant="outline" 
        onClick={()=>handleremovecompany(invoice.name)} 
        style={{ backgroundColor: "white", color: "black", width:10, height:30 }}
        >
        x
      </Button></TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
    </div>
  )
}
