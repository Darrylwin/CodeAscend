import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';
import 'app/core/di/service_locator.dart';
import 'app/core/routing/app_router.dart';
import 'app/core/themes/app_theme.dart';
import 'app/core/themes/theme_cubit.dart';
import 'app/features/auth/presentation/bloc/auth_bloc.dart';
import 'app/features/auth/presentation/bloc/auth_state.dart';

void main() async {
  //  Garder le splash natif visible
  WidgetsBinding widgetsBinding = WidgetsFlutterBinding.ensureInitialized();
  FlutterNativeSplash.preserve(widgetsBinding: widgetsBinding);

  // Initialiser les dépendances (GetIt)
  await initializeDependencies();

  // Initialiser les locales pour le formatage des dates
  await initializeDateFormatting('fr_FR', null);

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider<AuthBloc>(create: (_) => sl<AuthBloc>()),
        BlocProvider<ThemeCubit>(create: (_) => sl<ThemeCubit>()),
      ],
      child: BlocBuilder<ThemeCubit, ThemeMode>(
        builder: (context, themeMode) {
          return BlocBuilder<AuthBloc, AuthState>(
            builder: (context, authState) {
              final isAuthenticated = authState is Authenticated;
              final navigatorKey = sl<GlobalKey<NavigatorState>>();

              final router = AppRouter.router(
                isAuthenticated: isAuthenticated,
                authState: authState,
                navigatorKey: navigatorKey,
              );

              return MaterialApp.router(
                title: 'Code Ascend',
                debugShowCheckedModeBanner: false,
                theme: AppTheme.lightTheme,
                darkTheme: AppTheme.darkTheme,
                themeMode: themeMode,
                routerConfig: router,
              );
            },
          );
        },
      ),
    );
  }
}
