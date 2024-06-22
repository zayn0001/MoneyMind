// TextComponent.js
import { TypeAnimation } from 'react-type-animation';
 

const TextComponent = ({ value }) => {
  const seq = [value,1000,""]
    return (
      <h1 className="scroll-m-20 text-2xl text-center font-extrabold tracking-tight lg:text-2xl m-5" style={{maxWidth:"40%", minWidth:"200px"}}>
        
        <TypeAnimation
  sequence={seq}
  speed={25}
  style={{ fontSize: '2em' }}
  repeat={Infinity}
/>
      </h1>
    );
  };
  
  export default TextComponent;
  