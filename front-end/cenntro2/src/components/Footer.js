import React from 'react'
import EmailIcon from '@mui/icons-material/Email';
import "../styles/Footer.css";

function Footer() {
    return (
        <div className='footer'>
            <p>Thank you for visiting our website</p>
            <div className='socialMedia'>
                <EmailIcon /> <p>1234567@yahoo.com</p> <EmailIcon /> <p>1234567@yahoo.com</p><EmailIcon /> <p>1234567@yahoo.com</p>
                <EmailIcon /> <p>1234567@yahoo.com</p>
                <EmailIcon /> <p>1234567@yahoo.com</p>
            </div>
            <p className='copy'>&copy; 2021 utdcenntro.com</p>
        </div>
    )
}

export default Footer