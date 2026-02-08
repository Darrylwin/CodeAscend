//import node modules libraries
import { Fragment } from "react";
import { Metadata } from "next";

//import custom components
import QuizListHeader from "components/quiz/QuizListHeader";
import QuizList from "components/quiz/QuizList";

export const metadata: Metadata = {
    title: "Quiz List | Admin Dashboard",
    description: "Quiz Management for Programming App",
};

const QuizPage = () => {
    return (
        <Fragment>
            <QuizListHeader />
            <QuizList />
        </Fragment>
    );
};

export default QuizPage;
