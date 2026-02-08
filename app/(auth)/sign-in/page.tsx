"use client";

//import node modules libraries
import { Fragment, useState } from "react";
import Feedback from "react-bootstrap/Feedback";
import {
  Row,
  Col,
  Image,
  Card,
  CardBody,
  Form,
  FormLabel,
  FormControl,
  FormCheck,
  Button,
  Alert
} from "react-bootstrap";
import Link from "next/link";
import { useRouter } from "next/navigation";
// import { Metadata } from "next"; // Metadata cannot be used in client components
import {
  IconEyeOff,
  IconEye
} from "@tabler/icons-react";

//import custom components
import Flex from "components/common/Flex";

const SignIn = () => {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Authentication failed");
      }

      const data = await response.json();

      // Store token in localStorage for client-side access
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
        // Set cookie for server-side middleware/layout access
        document.cookie = `access_token=${data.access_token}; path=/; max-age=1800; SameSite=Lax`;
      }

      // Redirect to dashboard
      router.push("/");
      router.refresh();

    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Fragment>
      <Row className="mb-8">
        <Col xl={{ span: 4, offset: 4 }} md={12}>
          <div className="text-center">
            <h1 className="mb-1">Welcome Back</h1>
            <p className="mb-0">
              Don’t have an account yet?
              <Link href="#" className="text-primary ms-1">
                Register here
              </Link>
            </p>
          </div>
        </Col>
      </Row>

      {/* Form Start */}
      <Row className="justify-content-center">
        <Col xl={5} lg={6} md={8}>
          <Card className="card-lg mb-6">
            <CardBody className="p-6">
              {error && <Alert variant="danger">{error}</Alert>}
              <Form onSubmit={handleSubmit} className="mb-6">
                <div className="mb-3">
                  <FormLabel htmlFor="signinEmailInput">
                    Email <span className="text-danger">*</span>
                  </FormLabel>
                  <FormControl
                    type="email"
                    id="signinEmailInput"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <FormLabel htmlFor="formSignUpPassword">Password</FormLabel>
                  <div className="password-field position-relative">
                    <FormControl
                      type={showPassword ? "text" : "password"}
                      id="formSignUpPassword"
                      className="fakePassword"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                    <span
                      onClick={() => setShowPassword(!showPassword)}
                      style={{ cursor: "pointer" }}
                    >
                      {showPassword ? (
                        <IconEye className="passwordToggler" size={16} />
                      ) : (
                        <IconEyeOff className="passwordToggler" size={16} />
                      )}
                    </span>
                  </div>
                </div>
                <Flex
                  className="mb-4"
                  alignItems="center"
                  justifyContent="between"
                >
                  <FormCheck label="Remember me" type="checkbox" id="rememberMe" />
                  <div>
                    <Link href="" className="text-primary">
                      Forgot Password
                    </Link>
                  </div>
                </Flex>
                <div className="d-grid">
                  <Button variant="primary" type="submit" disabled={loading}>
                    {loading ? "Signing In..." : "Sign In"}
                  </Button>
                </div>
              </Form>

            </CardBody>
          </Card>
        </Col>
      </Row>
    </Fragment>
  );
};

export default SignIn;
