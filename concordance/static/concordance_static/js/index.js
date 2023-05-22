$(document).ready(function(){

////
//  RADIO TOGGLE ////
////
    counter = 0;
    $("#radio-case-specific").on("click", function(){
        counter += 1;
        if (counter % 2 === 0){
            $("#radio-case-specific").prop("checked", false);
        }
    })

////
//  FONT SELECTOR ////
////
    $("#font-selector").on("change", function(){
        const selected_value = $(this).val();
        
        // reset local storage
        CHOICES.forEach(choice => {
            localStorage.setItem(choice, "false")
            // remove classes 
            $("#container").removeClass(choice)
            $(".results").removeClass(choice)

            // always maintain at least large font for select menu
            if (choice !== "large-font"){
                $("#font-selector").removeClass(choice)
            }
        });

        // set local storage 
        localStorage.setItem(selected_value, "true")

        // remove large-font from navigation in case they choose normal-font
        $("#navigation a").removeClass("large-font")

        // If they did not choose normal-font,
        // set large-font for navigation
        if (selected_value !== "normal-font"){
            $("#navigation a").addClass("large-font")

            // never accept normal-font size for font select menu 
            $("#font-selector").addClass(selected_value)
        }

        // always set the container and results divs to select menu's option selected
        $("#container").addClass(selected_value)
        $(".results").addClass(selected_value)
    })

////
//  SET THE FONT SIZE ON PAGE LOAD ////
////
    const CHOICES = ["normal-font", "larger-font", "large-font", "largest-font"]
    CHOICES.forEach(choice => {
        if (localStorage.getItem(choice) === "true"){
            $("#container").addClass(choice)
            $(".results").addClass(choice)
            if (choice !== "normal-font"){
                $("#font-selector").addClass(choice)
                $("#navigation a").addClass("large-font")
            }
        }
    });
})
