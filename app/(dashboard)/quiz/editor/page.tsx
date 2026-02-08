//import node modules libraries
import { Fragment } from "react";
import { Metadata } from "next";

//import custom components
import QuizEditor from "components/quiz/QuizEditor";

export const metadata: Metadata = {
    title: "Editor Quiz | Admin Dashboard",
    description: "Quiz Editor for Programming App",
};

const QuizEditorPage = () => {
    return (
        <Fragment>
            <QuizEditor />
        </Fragment>
    );
};

export default QuizEditorPage;
