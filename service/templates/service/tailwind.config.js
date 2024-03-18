/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './*.html'
    ],
    theme: {
        extend: {
            colors: {
                'gray': {
                    500: '#525252'
                },
                'blue': {
                    50: '#EDF3F6',
                    400: '#5CBEF8',
                    410: '#6EBEEE',
                    450: '#1A8CD0',
                    500: '#0874B4',
                    600: '#2D5E7A',
                },
                'red': {
                    390: '#FFA896',
                    400: '#FF947E',
                    500: '#F1593A',
                    550: '#E34F31',
                }
            }
        },
        container: {
            center: true,
            screens: {
                sm: '576px',
                md: '768px',
                lg: '768px',
                xl: '1280px',
                '2xl': '1328px',
            },
            padding: {
                DEFAULT: '10px',
                sm: '24px',
                lg: '24px',
                xl: '24px',
                '2xl': '24px',
            },
        },
    },
    plugins: [],
}

