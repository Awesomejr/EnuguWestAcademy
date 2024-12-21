/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'

        // Flowbite
        './node_modules/flowbite/**/*.js',
    ],
    theme: {
        extend: {
            colors: {
                brightRed: "rgb(255, 0, 0)",
                black2: "rgba(0, 0, 0, 0.7)",
                black3: "rgba(0, 0, 0, 0.5)",
                black4: "rgba(0, 0, 0, 0.3)",
                myGreen: "rgb(18, 78, 36)",
                myWhite: "rgba(255, 255, 255, 1)",
                boneWhite: "#f9f6ee",
                black: "#0e1013",
                black8: "rgba(0, 0, 0, 0.8)",
                black6: "rgba(0, 0, 0, 0.6)",
                black4: "rgba(0, 0, 0, 0.4)",
                
                blackText: "#0e1013",
                
                blackBg: "#0e1013",
                boneWhiteBg: "#f9f6ee",
                brownBg: "rgb(24, 23, 23)",
                
                myBlue: "rgba(0, 0, 255, 0.8)",
                myRed: "rgba(255, 0, 0, 0.8)",
                myGreen: "#006400",
                myYellow: "rgb(194, 120, 3)",
                tableHeadBg: "rgb(5, 122, 85)",
                primaryBg: "rgb(1, 71, 55)",
            }
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),

        require('flowbite/plugin'),
    ],
}
