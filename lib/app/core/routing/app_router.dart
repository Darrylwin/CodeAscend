import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';

import '../../../main.dart';
import '../../features/auth/presentation/pages/profile_page.dart';
import '../di/service_locator.dart';
import '../../features/auth/presentation/pages/splash_page.dart';
import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/auth/presentation/pages/register_page.dart';
import '../../features/category/presentation/pages/home_page.dart';
import '../../features/category/presentation/pages/category_detail_page.dart';
import '../../features/category/presentation/pages/category_quizzes_page.dart';
import '../../features/category/presentation/bloc/category_bloc.dart';
import '../../features/category/presentation/bloc/category_event.dart';
import '../../features/category/presentation/bloc/category_state.dart';
import '../../features/quiz/presentation/pages/quiz_screen.dart';
import '../../features/quiz/presentation/pages/quiz_result_screen.dart';
import '../../features/quiz/presentation/pages/quiz_review_screen.dart';
import '../../features/quiz/presentation/bloc/quiz_bloc.dart';
import '../../features/quiz/presentation/bloc/quiz_event.dart';
import '../../features/auth/presentation/bloc/auth_state.dart';
import '../../features/attempts/presentation/pages/attempts_history_page.dart';
import '../../features/attempts/presentation/bloc/attempts_bloc.dart';
import '../../features/user_stats/presentation/pages/user_stats_page.dart';
import '../../features/user_stats/presentation/bloc/user_stats_bloc.dart';
import '../utils/route_observer.dart';
import '../widgets/scaffold_with_navbar.dart';

class AppRouter {
  AppRouter._();

  static const String splash = '/';
  static const String login = '/login';
  static const String register = '/register';
  static const String home = '/home';
  static const String history = '/history';
  static const String statistics = '/statistics';
  static const String profile = '/profile';
  static const String categoryDetail = '/category/:id';
  static const String categoryQuizzes = '/category/:id/quizzes';
  static const String quiz = '/quiz/:id';
  static const String quizResult = '/quiz/:id/result';
  static const String quizReview = '/quiz/:id/review';
  static const String attemptReview = '/attempt/:attemptId/review';

  static GoRouter createRouter({
    required AuthNotifier authNotifier,
    GlobalKey<NavigatorState>? navigatorKey,
  }) {
    return GoRouter(
      navigatorKey: navigatorKey,
      observers: [routeObserver],
      initialLocation: splash,
      debugLogDiagnostics: false,
      refreshListenable: authNotifier,
      redirect: (context, state) async {
        final authState = authNotifier.state;
        final currentLocation = state.matchedLocation;

        final isCheckingAuth =
            authState is AuthInitial || authState is AuthChecking;

        if (currentLocation == splash) {
          if (isCheckingAuth) return null;
          return authNotifier.isAuthenticated ? home : login;
        }

        final publicRoutes = [login, register];
        final isPublicRoute = publicRoutes.contains(currentLocation);

        if (!authNotifier.isAuthenticated && !isPublicRoute) return login;
        if (authNotifier.isAuthenticated &&
            isPublicRoute &&
            authState is Authenticated) return home;

        return null;
      },
      routes: [
        GoRoute(
          path: splash,
          name: 'splash',
          pageBuilder: (context, state) => MaterialPage<void>(
            key: state.pageKey,
            child: const SplashPage(),
          ),
        ),
        GoRoute(
          path: login,
          name: 'login',
          pageBuilder: (context, state) => MaterialPage<void>(
            key: state.pageKey,
            child: const LoginPage(),
          ),
        ),
        GoRoute(
          path: register,
          name: 'register',
          pageBuilder: (context, state) => MaterialPage<void>(
            key: state.pageKey,
            child: const RegisterPage(),
          ),
        ),

        // BottomNav shell
        StatefulShellRoute.indexedStack(
          builder: (context, state, navigationShell) =>
              ScaffoldWithNavBar(navigationShell: navigationShell),
          branches: [
            // Home
            StatefulShellBranch(routes: [
              GoRoute(
                path: home,
                pageBuilder: (context, state) => NoTransitionPage<void>(
                  key: state.pageKey,
                  child: MultiBlocProvider(
                    providers: [
                      BlocProvider(
                        create: (_) {
                          final bloc = sl<CategoryBloc>();
                          if (bloc.state is CategoryInitial) {
                            Future.delayed(Duration.zero, () {
                              if (!bloc.isClosed) {
                                bloc.add(const FetchCategories(isActive: true));
                              }
                            });
                          }
                          return bloc;
                        },
                      ),
                      BlocProvider.value(value: sl<AttemptsBloc>()),
                    ],
                    child: const HomePage(),
                  ),
                ),
              ),
            ]),

            // History
            StatefulShellBranch(routes: [
              GoRoute(
                path: history,
                pageBuilder: (context, state) => NoTransitionPage<void>(
                  key: state.pageKey,
                  child: BlocProvider.value(
                    value: sl<AttemptsBloc>(),
                    child: const AttemptsHistoryPage(),
                  ),
                ),
              ),
            ]),

            // Statistics
            StatefulShellBranch(routes: [
              GoRoute(
                path: statistics,
                pageBuilder: (context, state) => NoTransitionPage<void>(
                  key: state.pageKey,
                  child: BlocProvider.value(
                    value: sl<UserStatsBloc>(),
                    child: const UserStatsPage(),
                  ),
                ),
              ),
            ]),

            // Profile
            StatefulShellBranch(routes: [
              GoRoute(
                path: profile,
                pageBuilder: (context, state) => NoTransitionPage<void>(
                  key: state.pageKey,
                  child: const ProfileScreen(),
                ),
              ),
            ]),
          ],
        ),

        // Category detail (standalone)
        GoRoute(
          path: categoryDetail,
          name: 'categoryDetail',
          pageBuilder: (context, state) {
            final categoryId = state.pathParameters['id']!;
            return MaterialPage<void>(
              key: state.pageKey,
              child: MultiBlocProvider(
                providers: [
                  BlocProvider(create: (_) => sl<CategoryBloc>()),
                  BlocProvider.value(value: sl<AttemptsBloc>()),
                ],
                child: CategoryDetailPage(categoryId: categoryId),
              ),
            );
          },
        ),

        GoRoute(
          path: categoryQuizzes,
          name: 'categoryQuizzes',
          pageBuilder: (context, state) {
            final categoryId = state.pathParameters['id']!;
            final level = state.uri.queryParameters['level'];
            return MaterialPage<void>(
              key: state.pageKey,
              child: BlocProvider(
                create: (_) => sl<CategoryBloc>(),
                child: Builder(builder: (context) {
                  return BlocBuilder<CategoryBloc, CategoryState>(
                    builder: (context, catState) {
                      if (catState is CategoryLoading ||
                          catState is CategoryInitial) {
                        return const Scaffold(
                            body: Center(child: CircularProgressIndicator()));
                      }
                      if (catState is CategoryError) {
                        return Scaffold(
                            appBar: AppBar(title: const Text('Quizzes')),
                            body: Center(child: Text(catState.message)));
                      }
                      if (catState is CategoryLoaded) {
                        return CategoryQuizzesPage(
                          categoryId: categoryId,
                          level: level,
                          quizzes: catState.quizzes,
                        );
                      }
                      return const SizedBox.shrink();
                    },
                  );
                }),
              ),
            );
          },
        ),

        GoRoute(
          path: quiz,
          name: 'quiz',
          pageBuilder: (context, state) {
            final quizId = state.pathParameters['id']!;
            final restore = state.uri.queryParameters['restore'] == 'true';
            return MaterialPage<void>(
              key: state.pageKey,
              child: BlocProvider<QuizBloc>(
                create: (_) {
                  final bloc = sl<QuizBloc>();
                  if (restore) {
                    bloc.add(QuizRestoreRequested(quizId));
                  } else {
                    bloc.add(QuizLoadRequested(quizId));
                  }
                  return bloc;
                },
                child: _QuizScreenWrapper(quizId: quizId),
              ),
            );
          },
          routes: [
            GoRoute(
              path: 'result',
              name: 'quizResult',
              pageBuilder: (context, state) {
                final quizId = state.pathParameters['id']!;
                final attemptId = state.uri.queryParameters['attemptId'] ?? '';
                return MaterialPage<void>(
                  key: state.pageKey,
                  child: QuizResultScreen(
                    quizId: quizId,
                    attemptId: attemptId,
                    queryParams: state.uri.queryParameters,
                  ),
                );
              },
            ),
            GoRoute(
              path: 'review',
              name: 'quizReview',
              pageBuilder: (context, state) {
                final quizId = state.pathParameters['id']!;
                final attemptId = state.uri.queryParameters['attemptId'] ?? '';
                return MaterialPage<void>(
                  key: state.pageKey,
                  child: QuizReviewScreen(
                    quizId: quizId,
                    attemptId: attemptId,
                    queryParams: state.uri.queryParameters,
                  ),
                );
              },
            ),
          ],
        ),

        GoRoute(
          path: attemptReview,
          name: 'attemptReview',
          pageBuilder: (context, state) {
            final attemptId = state.pathParameters['attemptId']!;
            return MaterialPage<void>(
              key: state.pageKey,
              child: QuizReviewScreen(
                attemptId: attemptId,
                queryParams: state.uri.queryParameters,
              ),
            );
          },
        ),
      ],
      errorBuilder: (context, state) => Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 64, color: Colors.red),
              const SizedBox(height: 16),
              Text('Page non trouvée',
                  style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 8),
              Text(state.error.toString(), textAlign: TextAlign.center),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () => context.go(home),
                child: const Text('Retour à l\'accueil'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _QuizScreenWrapper extends StatelessWidget {
  final String quizId;
  const _QuizScreenWrapper({required this.quizId});

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        final shouldPop = await showDialog<bool>(
          context: context,
          barrierDismissible: false,
          builder: (dialogContext) => AlertDialog(
            title: Row(
              children: [
                Icon(Icons.info_outline_rounded,
                    color: Theme.of(context).colorScheme.primary, size: 28),
                const SizedBox(width: 12),
                const Expanded(child: Text('Quitter le quiz ?')),
              ],
            ),
            content: const Text(
              'Votre progression sera sauvegardée. '
              'Vous pourrez reprendre ce quiz plus tard.',
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(dialogContext).pop(true),
                child: Text('Quitter',
                    style: TextStyle(
                        color: Theme.of(context).colorScheme.error,
                        fontWeight: FontWeight.w500)),
              ),
              ElevatedButton(
                onPressed: () => Navigator.of(dialogContext).pop(false),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Theme.of(context).colorScheme.primary,
                  foregroundColor: Theme.of(context).colorScheme.onPrimary,
                  padding:
                      const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                ),
                child: const Text('Continuer le quiz'),
              ),
            ],
            actionsAlignment: MainAxisAlignment.spaceBetween,
          ),
        );
        if (shouldPop == true && context.mounted) {
          context.go(AppRouter.home);
        }
        return false;
      },
      child: QuizScreen(quizId: quizId),
    );
  }
}
